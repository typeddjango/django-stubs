#! /usr/bin/env bash

set -euxo pipefail
cleanup() {
    git remote remove tmp_upstream > /dev/null
    if [ ! -z $cur_branch ]; then
        git checkout $cur_branch > /dev/null
    fi
}

cur_branch=$(git branch --show-current)

# Will compare to master.
git remote add tmp_upstream https://github.com/typeddjango/django-stubs || (cleanup && exit 2)
git fetch tmp_upstream --quiet

# Fetch last cache.
mkdir -p .custom_cache/
cur_hash=$(git rev-parse HEAD)  # Actual commit we're testing
git fetch tmp_upstream refs/notes/*:refs/notes/*  --quiet # Use * so that it won't fail on first run
ref_branch=tmp_upstream/master

# Try to compare with master
ref_hash=$(git rev-parse $ref_branch)
if [ "$ref_hash" = "$cur_hash" ]; then
    # Already on master; compare to previous commit
    ref_hash=$(git rev-parse $ref_branch^)
fi

# Get result of run on ref_hash (should fail on first workflow run)
git notes --ref cache_history show $ref_hash > .custom_cache/.apply_errors && true
if [ $? -eq 0 ]; then
    ./scripts/compare_errors.py && true
    result=$?
else
    echo 'No data for main branch yet - nothing to do.'
    result=0
fi

./scripts/write_errors_cache.py
cleanup
exit $result
