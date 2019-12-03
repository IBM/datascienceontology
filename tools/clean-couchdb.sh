#!/usr/bin/env sh
set -e

DIR=$(dirname $0)
PATH=$PWD/node_modules/.bin:$PATH
TMP_DELETE_FILE=$DIR/../build/deletion.json

ccurl /data-science-ontology/_all_docs | jq '.rows |
    map(. as { id: $id, value: { rev: $rev } } |
        select($id | test("^_design/") | not) |
        { _id: $id, _rev: $rev, _deleted: true }) |
        { docs: . }' \
    > $TMP_DELETE_FILE
ccurl -X POST -d @$TMP_DELETE_FILE /data-science-ontology/_bulk_docs | jq '.'
