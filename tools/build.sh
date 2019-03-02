#!/usr/bin/env bash
set -e

DIR=$(dirname $0)
cd "$DIR/.."
PATH="node_modules/.bin:$PATH"

# Create build directory structure.
rm -rf build
find concept annotation references -type d | xargs -I{} mkdir -p "build/{}"

# Convert YAML concept and annotation documents to JSON.
find concept annotation -name '*.yml' | while read yml; do
    js-yaml "$yml" > "build/${yml%.yml}.json"
done

# Convert BibTeX references to CSL JSON.
find references -name '*.bib' | while read bib; do
    pandoc-citeproc --bib2json "$bib" > "build/${bib%.bib}.json"
done
