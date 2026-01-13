#!/bin/sh

# Run this script with `./scripts/stubtest.sh`

set -e

export MYPYPATH='.'

# Cleaning existing cache:
rm -rf .mypy_cache

stubtest django \
    --mypy-config-file mypy.ini \
    --allowlist scripts/stubtest/allowlist.txt \
    --allowlist scripts/stubtest/allowlist_todo.txt \
    --allowlist scripts/stubtest/allowlist_todo_django52.txt
