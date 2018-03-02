#!/usr/bin/env bash
DIR=$(dirname $0)

ajv --errors=json -s "$DIR/schemas/concept.json" -d "concept/*.json"
(( STATUS = STATUS || $? ))

ajv --errors=json -s "$DIR/schemas/annotation.json" -d "annotation/**/*.json"
(( STATUS = STATUS || $? ))

exit $STATUS
