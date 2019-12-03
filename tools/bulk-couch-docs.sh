#!/usr/bin/env bash
set -e

DIR=$(dirname $0)
PATH="node_modules/.bin:$PATH"
TMP_DOCS_FILE="$DIR/../build/all-docs.json"

"$DIR/make-couch-docs.sh" | jq '{docs: .}' > $TMP_DOCS_FILE
ccurl -X POST -d @$TMP_DOCS_FILE /data-science-ontology/_bulk_docs | jq '.'
