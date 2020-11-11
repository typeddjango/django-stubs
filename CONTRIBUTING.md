# Contribution Guide

This project is open source and community driven. As such we encourage code contributions of all kinds. Some areas you can contribute in:

1. Improve the stubs
2. Sync stubs with the latest version of Django
3. Improve plugin code and extend its capabilities
4. Write tests
5. Update dependencies

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
In order to be able to continously sync your fork with the origin repository's master branch, you will need to set up an upstream master. To do so follow this [official github guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

### Dependency Setup

After your repository is setup you will then need to create and activate a git ignored virtual env, e.g.:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install the dev requirements:

```bash
pip install -r ./dev-requirements.txt
```

Finally, install the pre-commit hooks:

```bash
pre-commit install
```

### Testing and Linting

We use `mypy`, `pytest`, `flake8`, and `black` for quality control. All tools except pytest are executed using pre-commit when you make a commit.
To ensure there are not formatting or typing issues in the entire repository you can run:

```bash
pre-commit run --all-files
```

NOTE: This command will not only lint but also modify files - so make sure to commit whatever changes you've made before hand.
You can also run pre-commit per file or for a specific path, simply replace "--all-files" with a target (see [this guide](https://codeburst.io/tool-your-django-project-pre-commit-hooks-e1799d84551f) for more info).

To execute the unit tests, simply run:

```bash
pytest
```

We also test the stubs against the Django's own test suite. This is done in CI but you can also do this locally.
To execute the script run:

```bash
python ./scripts/typecheck_tests.py --django_version 3.0
```


### Generating Stubs using Stubgen

The stubs are based on auto-generated code created by Mypy's stubgen tool (see: [the stubgen docs](https://mypy.readthedocs.io/en/stable/stubgen.html)).
To make life easier we have a helper script that auto generates these stubs. To use it you can run:

```bash
python ./scripts/stubgen-django.py --django_version 3.1
```

You can also pass an optional commit hash as a second kwarg to checkout a specific commit, e.g.

```bash
python ./scripts/stubgen-django.py --django_version 3.1 --commit_sha <commit_sha>
```

The output for this is a gitignored folder called "stubgen" in the repo's root.

## Submission Guidelines

The workflow for contributions is fairly simple:

1. fork and setup the repository as in the previous step.
2. create a local branch.
3. make whatever changes you want to contribute.
4. ensure your contribution does not introduce linting issues or breaks the tests by linting and testing the code.
5. make a pull request with an adequate description.

## A Note About Generics

As Django uses a lot of the more dynamic features of Python (i.e. metaobjects), statically typing it requires heavy use of generics. Unfortunately, the syntax for generics is also valid python syntax. For instance, the statement `class SomeClass(SuperType[int])` implicitly translates to `class SomeClass(SuperType.__class_getitem__(int))`. If `SuperType` doesn't define the `__class_getitem__` method, this causes a runtime error, even if the code typechecks.

When adding a new generic class, or changing an existing class to use generics, run a quick test to see if it causes a runtime error. If it does, please add the new generic class to the `_need_generic` list in the [django_stubs_ext monkeypatch function](https://github.com/typeddjango/django-stubs/tree/master/django_stubs_ext/django_stubs_ext/monkeypatch.py)
