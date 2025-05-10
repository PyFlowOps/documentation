#!/usr/bin/env bash

set -eou pipefail

BASE=$(dirname "$0")

# Diff HEAD with the previous commit
diff=( $(git diff --name-only HEAD^ HEAD) )

# Check if the diff contains any markdown files
if [[ ${diff[*]} =~ .*\.md ]]; then
    return 0
else
    return 1
fi
