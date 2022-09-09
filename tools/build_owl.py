from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml
from bioontologies.robot import convert
from pyobo import Obo, Reference, Term, TypeDef
from pyobo.struct import part_of

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
BUILD = ROOT.joinpath("exports")
BUILD.mkdir(parents=True, exist_ok=True)
PREFIX = "dso"

# implemented_by = TypeDef.from_triple("SWO", "0000085", "is implemented by")
implemented_in = TypeDef.from_triple(PREFIX, "implemented_in", "is implemented in")

language = Term.from_triple("IAO", "0000025", "programming language")

starters = {
    "function": "Function",
    "type": "Type",
    "language": "Language",
    "package": "Package",
    "r-package": "R Package",
    "python-package": "Python Package",
}

languages = {
    "r": Term.from_triple("SWO", "0000415", "R language").append_parent(language),
    "python": Term.from_triple("SWO", "0000118", "Python").append_parent(language),
    "language": language,
}

def get_terms():
    """"""
    concepts = {
        identifier: Term.from_triple(PREFIX, identifier, name)
        for identifier, name in starters.items()
    }
    concepts.update(languages)
    parents = defaultdict(set)
    outputs = defaultdict(list)
    inputs_dict = defaultdict(list)
    kinds = {}
    for path in ROOT.joinpath("concept").glob("*.yml"):
        data = yaml.safe_load(path.read_text())
        identifier = data.pop("id")
        kinds[identifier] = data.pop("kind")
        inputs_dict[identifier] = data.pop("inputs", [])
        outputs[identifier] = data.pop("outputs", [])

        # this refers to keys in the bib files.
        # there are only 4 such annotations, so skip for now
        data.pop("references", None)

        parent = data.pop("is-a", None)
        if parent:
            if isinstance(parent, list):
                parents[identifier].update(parent)
            elif isinstance(parent, str):
                parents[identifier].add(parent)
            else:
                raise ValueError(parent)

        definition = data.pop("description", None)
        if definition is not None:
            definition = definition.strip()

        concepts[identifier] = Term(
            reference=Reference(
                prefix=PREFIX,
                identifier=identifier,
                name=data.pop("name").strip(),
            ),
            definition=definition,
            namespace=data.pop("schema"),
            xrefs=[
                Reference(prefix=xref_prefix, identifier=xref_identifier)
                for xref_prefix, xref_identifier in data.pop("external", {}).items()
            ],
        )

    # Back-fill parents
    for child, parents in parents.items():
        for parent in parents:
            concepts[child].append_parent(concepts[parent])

    # For concepts that never got a parent, add the "kind"
    for term in concepts.values():
        if term.identifier in starters or term.prefix != PREFIX:
            continue
        if not term.parents:
            term.append_parent(concepts[kinds[term.identifier]])

    # Annotate inputs
    for identifier, inputs in inputs_dict.items():
        for i, d in enumerate(inputs):
            input_type = d.pop("type")
            if input_type not in concepts:
                print(
                    f"could not look up input type for {identifier}: [{i}] {input_type}"
                )
            else:
                # TODO
                pass

    for language_directory in ROOT.joinpath("annotation").iterdir():
        if not language_directory.is_dir():
            continue
        language_term = concepts[language_directory.name]
        language_package_key = f"{language_directory.name}-package"
        language_package_term = concepts[language_package_key] = Term.from_triple(
            PREFIX,
            language_package_key,
            f"{language_directory.name} Package",
        )
        language_package_term.append_parent(concepts["package"])
        language_package_term.append_relationship(implemented_in, language_term)
        for package_directory in language_directory.iterdir():
            if not package_directory.is_dir():
                continue
            package_term = concepts[package_directory.name] = Term.from_triple(
                PREFIX, package_directory.name, f"{package_directory.name} Package"
            )
            package_term.append_parent(language_package_term)

    annotations = {}
    for path in HERE.joinpath("annotation").glob("*/*/*.yml"):
        data = yaml.safe_load(path.read_text())
        identifier = data.pop("id")

        term = annotations[identifier] = Term(
            reference=Reference(
                PREFIX,
                identifier,
                name=data.pop("name", identifier),
            ),
            definition=data.pop("description", None),
            namespace=data.pop("schema"),
        )
        term.append_parent(data.pop("type"))
        term.append_relationship(part_of, concepts[data.pop("package")])
        data.pop("language", None)  # don't need, can be inferred from package

    return [*concepts.values(), *annotations.values()]


def get_ancestors(concepts: dict[str, Term], term: Term) -> Iterable[Term]:
    """Get all parents."""
    for parent in term.parents:
        yield concepts[parent.identifier]
        yield from get_ancestors(concepts, concepts[parent.identifier])


class DataScienceOntologyGetter(Obo):
    """An ontology representation of the Data Science Ontology."""

    ontology = PREFIX
    name = "Data Science Ontology"
    static_version = "1.0"
    typedefs = [part_of, implemented_in]

    def iter_terms(self, force: bool = False) -> Iterable[Term]:
        """Iterate over terms in the ontology."""
        return get_terms()


def main():
    obo = DataScienceOntologyGetter()
    obo_path = BUILD.joinpath("dso.obo")
    owl_path = BUILD.joinpath("dso.owl")
    json_path = BUILD.joinpath("dso.json")
    obo.write_obo(obo_path)
    convert(obo_path, owl_path)
    convert(obo_path, json_path)


if __name__ == "__main__":
    main()
