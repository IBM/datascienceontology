#!/usr/bin/env bash
set -e

DIR=$(dirname $0)
cd "$DIR/../build"

{ 
    find concept -name "*.json" -exec cat {} + |
        jq '{_id: ("concept/"+.id)} + .';
    
    find annotation -name "*.json" -exec cat {} + |
        jq '{_id: ("annotation/"+.language+"/"+.package+"/"+.id)} + .';
    
    find references -name "*.json" -exec cat {} + |
        jq '.[]' | jq '{_id: ("reference/"+.id), schema: "csl-data-item"} + .';
} |
    jq -s '.'
