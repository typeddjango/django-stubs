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
pre-mr-check: lint typecheck-all mypy-self stubtest ext-test test

# Remove mypy cache
[group('dev')]
clean-cache:
    rm -rf .mypy_cache
    rm -rf .pytest_cache
    rm -rf .ruff_cache

# Run mypy on the internal python code.
[group('typecheck')]
mypy-self:
    uv run mypy ext scripts mypy_django_plugin
    uv run mypy --cache-dir=/dev/null --no-incremental django-stubs

# Run mypy on test cases (default), or on the given files
[group('typecheck')]
mypy *files="tests/assert_type":
    uv run mypy {{ files }}

# Run pyright on test cases (default), or on the given files
[group('typecheck')]
pyright *files="tests/assert_type":
    uv run pyright {{ files }}

# Run pyrefly on test cases (default), or on the given files
[group('typecheck')]
pyrefly *files="tests/assert_type":
    uv run pyrefly check {{ files }}

# Run ty on test cases (default), or on the given files
[group('typecheck')]
ty *files="tests/assert_type":
    uv run ty check {{ files }}

# Run all typecheckers on test cases (default), or on the given files
[group('typecheck')]
typecheck-all *files="tests/assert_type": (pyrefly files) (ty files) (pyright files) (mypy files)

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
