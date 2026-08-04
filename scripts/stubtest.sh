#!/bin/sh

# Run this script with `./scripts/stubtest.sh [additional_stubtest_args]`

set -e

export MYPYPATH='.'

# Getting per version allowlist file:
PYTHON_VERSION="$(python --version 2>&1 | sed 's/Python \([0-9]*\)\.\([0-9]*\)\..*/\1\2/')"
PYTHON_VERSION_ALLOWLIST="scripts/stubtest/allowlist_python${PYTHON_VERSION}.txt"
if [ -f "$PYTHON_VERSION_ALLOWLIST" ]; then
    VERSION_SPECIFIC_ALLOWLIST="--allowlist $PYTHON_VERSION_ALLOWLIST"
else
    VERSION_SPECIFIC_ALLOWLIST=
fi

# Cleaning existing cache:
rm -rf .mypy_cache

stubtest django \
    --mypy-config-file mypy.ini \
    --allowlist scripts/stubtest/allowlist.txt \
    --allowlist scripts/stubtest/allowlist_todo.txt \
    $VERSION_SPECIFIC_ALLOWLIST \
    "$@"
