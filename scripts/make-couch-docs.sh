#!/usr/bin/env bash
set -e

find concept annotation -name "*.json" -exec cat {} + |
    jq -s '.'
