#!/usr/bin/env bash
set -e
DIR=$(dirname $0)

{ 
    find "$DIR/../concept" -name "*.json" -exec cat {} + |
        jq '{_id: ("concept/"+.ontology+"/"+.id)} + .';
    
    find "$DIR/../annotation" -name "*.json" -exec cat {} + |
        jq '{_id: ("annotation/"+.language+"/"+.package+"/"+.id)} + .';
} |
    jq -s '.'
