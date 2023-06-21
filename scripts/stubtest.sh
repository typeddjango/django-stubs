#!/usr/bin/env bash

# Run this script as `bash ./scripts/stubtest.sh`

set -e

export MYPYPATH='.'

# TODO: remove `--ignore-positional-only` and ``--ignore-missing-stubs when ready
stubtest django \
    --mypy-config-file mypy.ini \
    --ignore-positional-only \
    --ignore-missing-stubs \
    --allowlist scripts/stubtest/allowlist.txt \
    --allowlist scripts/stubtest/allowlist_generated.txt \
    --generate-allowlist
