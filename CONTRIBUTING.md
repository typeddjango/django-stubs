# Contribution Guide

This project is open source and community driven. As such we encourage code contributions of all kinds. Some areas you can contribute in:

1. Improve the stubs
2. Sync stubs with the latest version of Django
3. Improve plugin code and extend its capabilities
4. Write tests
5. Update dependencies
6. Fix and remove things from our `scripts/stubtest/allowlist_todo.txt`

## Tutorials

If you want to start working on this project, you will need to get familiar with python typings.
The Mypy documentation offers an excellent resource for this, as well as the python official documentation:

- [Mypy typing documentation](https://mypy.readthedocs.io/en/stable/#overview-type-system-reference)
- [Python official typing documentation](https://docs.python.org/3/library/typing.html)
- [Typing in Python](https://inventwithpython.com/blog/2019/11/24/type-hints-for-busy-python-programmers/) article

Additionally, the following resources might be useful:

- [How to write custom mypy plugins](https://mypy.readthedocs.io/en/stable/extending_mypy.html)
- [Typechecking Django and DRF](https://sobolevn.me/2019/08/typechecking-django-and-drf) guide
- [Testing mypy stubs, plugins, and types](https://sobolevn.me/2019/08/testing-mypy-types) guide
- [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing) list

## Dev setup

### Repository Setup

As a first step you will need to fork this repository and clone your fork locally.
In order to be able to continuously sync your fork with the origin repository's master branch, you will need to set up an upstream master.
To do so follow this [official github guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

### System Dependencies

The test suite requires some system libraries that Django itself treats as optional.
This project depends on `mysqlclient`, which needs MySQL/MariaDB C client libraries to build.
Install them for your platform following the
[mysqlclient install guide](https://github.com/PyMySQL/mysqlclient#install).
For Debian/Ubuntu, the [django-docker-box packages list](https://github.com/django/django-docker-box/blob/main/packages.txt)
is also a useful reference.

**GDAL and GEOS** are needed to pass all tests (2 GIS-related tests require them).
See the Django documentation on
[installing geospatial libraries](https://docs.djangoproject.com/en/stable/ref/contrib/gis/install/geolibs/).
If you're not working on GIS-related stubs, you can skip GDAL/GEOS —
the 2 failing tests won't affect other contributions.

> **macOS Note:** Homebrew installs GDAL/GEOS to `/opt/homebrew` (Apple Silicon) or `/usr/local` (Intel),
> which are not in the default library search path. The GIS tests may fail unless you create symlinks:
>
> ```bash
> sudo mkdir -p /usr/local/lib
> sudo ln -s /opt/homebrew/opt/gdal/lib/libgdal.dylib /usr/local/lib/libgdal.dylib
> sudo ln -s /opt/homebrew/opt/geos/lib/libgeos_c.dylib /usr/local/lib/libgeos_c.dylib
> ```

### Dependency Setup

We use [uv](https://github.com/astral-sh/uv) to manage our dev dependencies.
To install it, see their [installation guide](https://docs.astral.sh/uv/getting-started/installation/)

We use [just](https://github.com/casey/just) as a command runner. Install it with:

```bash
uv tool install rust-just
```

Then bootstrap your environment (installs pre-commit hooks and syncs dependencies):

```bash
just bootstrap
```

<details>
<summary>Manual setup (without <code>just</code>)</summary>

```bash
uv sync
source .venv/bin/activate
pre-commit install --install-hooks
```
</details>

### Testing and Linting

Running `just` at the root of the repository lists all available recipes:

```
$ just
Available recipes:
    [dev]
    bootstrap      # Bootstrap dev environment: install pre-commit hooks and sync dependencies
    lint           # Run pre-commit hooks on all files
    pre-mr-check   # Run all checks before submitting a PR
    clean          # Remove mypy cache

    [typecheck]
    mypy           # Run mypy on plugin, ext, scripts, stubs and tests
    pyright        # Run pyright on test cases
    pyrefly        # Run pyrefly on test cases
    ty             # Run ty on test cases

    [test]
    test +args     # Run pytest on specific files or with custom args (no xdist)
    all-test       # Run full pytest test suite with parallel workers
    stubtest *args # Run stubtest to check stubs match runtime
    ext-test       # Run django-stubs-ext tests

    [build]
    build          # Build all packages
    lock-check     # Check that uv.lock is up to date
```

Before submitting a PR, run all checks at once:

```bash
just pre-mr-check
```

Or run individual checks:

```bash
just lint          # pre-commit hooks (ruff, codespell, ...)
just mypy          # mypy on plugin, ext, scripts, stubs and tests
just test tests/test_xyz.yml  # run specific tests (no xdist)
just all-test      # full pytest suite (parallel)
just stubtest      # stubtest: check stubs match runtime
just pyright       # pyright on test cases
just ty            # ty on test cases
just pyrefly       # pyrefly on test cases
```

Extra arguments can be passed to `test` and `stubtest`:

```bash
just test tests -k test_name
just stubtest --allowlist extra.txt
```

If you get unexpected results, clear the mypy cache with `just clean`.

### Debugging plugin code

For yml tests, we use a dedicated [pytest plugin](https://github.com/typeddjango/pytest-mypy-plugins) that is by default
running mypy in a subprocess, making it difficult to debug.
To avoid that, run pytest with the `--mypy-same-process` flag.

```shell
pytest --mypy-same-process tests/typecheck/managers/querysets/test_annotate.yml
```

### Testing stubs with `stubtest`

Run `just stubtest` (or [`./scripts/stubtest.sh`](scripts/stubtest.sh) directly) to test that stubs and sources are in-line.

We have some special files to allow errors:

1. [`scripts/stubtest/allowlist.txt`](scripts/stubtest/allowlist.txt) - Permanent exclusions, e.g. internal utilities, plugin-handled items, type system limitations.
2. [`scripts/stubtest/allowlist_todo.txt`](scripts/stubtest/allowlist_todo.txt) - General backlog of stub errors to fix or move to permanent allowlist.

You might also want to disable `incremental` mode while working on `stubtest` changes.
This mode leads to several known problems (stubs do not show up or have strange errors).

## Submission Guidelines

The workflow for contributions is fairly simple:

1. Fork and set up the repository as in the previous step.
2. Create a local branch.
3. Make whatever changes you want to contribute.
4. Ensure your contribution passes linting and tests.
5. Make a pull request with an adequate description.

## Generics

As Django uses a lot of the more dynamic features of Python (i.e. metaobjects), statically typing it requires heavy use of generics.
Unfortunately, the syntax for generics is also valid Python syntax.
For instance, the statement `class SomeClass(SuperType[int])` implicitly translates to `class SomeClass(SuperType.__class_getitem__(int))`.
If `SuperType` doesn't define the `__class_getitem__` method, this causes a runtime error, even if the code passes type checking.

When adding a new generic class, or changing an existing class to use generics, run a quick test to see if it causes a runtime error.
If it does, please add the new generic class to the `_need_generic` list in the [`django_stubs_ext.patch` module](https://github.com/typeddjango/django-stubs/blob/master/ext/django_stubs_ext/patch.py).

## Private attributes

We only add hints for private attributes when it has some demonstrated real-world use case.
That means from a third-party package or some well described snippet for a project.
This rule helps us avoid tying in too closely to Django’s undocumented internals.

## Releasing `django-stubs`

1. Open a pull request that updates `pyproject.toml`, `ext/pyproject.toml` and `README.md`
   (anyone can open this PR, not just maintainers):

    - Version number `major.minor.patch` is formed as follows:

      `major.minor` version must match newest supported Django release.

      `patch` is sequentially increasing for each stubs release. Reset to `0` if `major.minor` was updated.

    - Update the `version =` value within `[project]` section in **both** `pyproject.toml` files. The versions must be in sync.
    - Update `django-stubs-ext>=` dependency in root `pyproject.toml` to the same version number.
    - Run `uv lock` to update lockfile
    - Add a new row at the top of ['Version compatibility' table in README.md](README.md#version-compatibility).
    - Use pull request title "Version x.y.z release" by convention.
    - Add the correct classifiers to `classifiers =` if support is added for a new Python or Django version

2. Ensure the CI succeeds. A maintainer must merge this PR. If it's just a version bump, no need
   to wait for a second maintainer's approval.

3. A maintainer must [сreate a new GitHub release](https://github.com/typeddjango/django-stubs/releases/new):

    - Under "Choose a tag" enter the new version number. Do **not** use `v` prefix.
    - Click "Generate release notes".
    - Look for merged PRs with the ['release notes reminder' label](https://github.com/typeddjango/django-stubs/issues?q=is%3Aopen+is%3Aissue+label%3A%22release+notes+reminder%22)
      and move them to a separate section at the top, so that they stand out. Remove the label from PRs.
    - Delete all release notes lines containing `by @pre-commit-ci` or `by @dependabot`, as these
      are irrelevant for our users.

4. Once you feel brave enough, click "Publish release".

5. Check that the [release workflow](https://github.com/typeddjango/django-stubs/actions/workflows/release.yml) succeeds.
