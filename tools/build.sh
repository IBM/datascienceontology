#!/usr/bin/env bash
set -e

DIR=$(dirname $0)
cd "$DIR/.."

# Create build directory structure.
mkdir -p build
find concept annotation -type d | xargs -I{} mkdir -p "build/{}"

# Convert YAML documents to JSON.
find concept annotation -name '*.yml' | while read yml; do
    yq '.' "$yml" > "build/${yml%.yml}.json"
done

