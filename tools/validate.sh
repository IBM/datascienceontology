#!/usr/bin/env bash

DIR=$(dirname $0)
cd "$DIR/../build"

ajv --errors=json -s "../tools/schemas/concept.json" -d "concept/*.json"
(( STATUS = STATUS || $? ))

ajv --errors=json -s "../tools/schemas/annotation.json" -d "annotation/**/*.json"
(( STATUS = STATUS || $? ))

exit $STATUS
