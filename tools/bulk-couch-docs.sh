#!/usr/bin/env bash
set -e
DIR=$(dirname $0)

"$DIR/make-couch-docs.sh" |
    jq '{docs: .}' |
    ccurl -X POST -d @- /data-science-ontology/_bulk_docs |
    jq '.'
