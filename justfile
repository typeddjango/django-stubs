# List all available recipes
_default:
    @just --list --unsorted

# Bootstrap dev environment: install pre-commit hooks and sync dependencies
[group('dev')]
bootstrap:
    uv tool install pre-commit
    uv sync
    pre-commit install --install-hooks

# Run pre-commit hooks on all files
[group('dev')]
lint:
    pre-commit run --all-files

# Run all checks before submitting a PR
[group('dev')]
pre-mr-check: lint typecheck-all stubtest ext-test test

# Remove mypy cache
[group('dev')]
clean:
    rm -rf .mypy_cache

# Run mypy on plugin, ext, scripts, stubs and tests
[group('typecheck')]
mypy:
    uv run mypy ext scripts mypy_django_plugin tests
    uv run mypy --cache-dir=/dev/null --no-incremental django-stubs

# Run pyright on test cases
[group('typecheck')]
pyright:
    uv run pyright

# Run pyrefly on test cases
[group('typecheck')]
pyrefly:
    uv run pyrefly check tests/assert_type

# Run ty on test cases
[group('typecheck')]
ty:
    uv run ty check tests/assert_type

# Run all typechecker on test cases
[group('typecheck')]
typecheck-all: pyrefly ty pyright mypy

# Run pytest tests
[group('test')]
test +args="-n auto tests":
    uv run pytest {{ args }}

# Run stubtest to check stubs match runtime
[group('test')]
stubtest *args:
    uv run ./scripts/stubtest.sh {{ args }}

# Run django-stubs-ext tests
[group('test')]
ext-test:
    uv run pytest ext

# Build all packages
[group('build')]
build:
    uv build --all-packages

# Check that uv.lock is up to date
[group('build')]
lock-check:
    uv lock --check
