#!/usr/bin/env bash

# Run this script as `bash ./scripts/stubtest.sh`

set -e

export MYPYPATH='.'

# Cleaning existing cache:
rm -rf .mypy_cache

# TODO: remove `--ignore-positional-only` when ready
stubtest django \
    --mypy-config-file mypy.ini \
    --ignore-positional-only \
    --allowlist scripts/stubtest/allowlist.txt \
    --allowlist scripts/stubtest/allowlist_todo.txt \
    --allowlist scripts/stubtest/allowlist_todo_django51.txt
