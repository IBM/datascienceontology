#!/usr/bin/env bash

DIR=$(dirname $0)
cd "$DIR/.."
PATH="node_modules/.bin:$PATH"

ajv --errors=json -s "tools/schemas/concept.json" -d "build/concept/*.json"
(( STATUS = STATUS || $? ))

ajv --errors=json -s "tools/schemas/annotation.json" -d "build/annotation/**/*.json"
(( STATUS = STATUS || $? ))

exit $STATUS
