#!/usr/bin/env bash
set -e

DIR=$(dirname $0)
cd "$DIR/.."
PATH="node_modules/.bin:$PATH"

# Create build directory structure.
rm -rf build
find concept annotation -type d | xargs -I{} mkdir -p "build/{}"

# Convert YAML documents to JSON.
find concept annotation -name '*.yml' | while read yml; do
    js-yaml "$yml" > "build/${yml%.yml}.json"
done
