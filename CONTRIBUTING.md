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
In order to be able to continuously sync your fork with the origin repository's master branch, you will need to set up an upstream master. To do so follow this [official github guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

### Dependency Setup

After your repository is setup you will then need to create and activate a git ignored virtual env, e.g.:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then install the dev requirements:

```bash
pip install -r ./requirements.txt
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

If you get some unexpected results or want to be sure that tests run is not affected by previous one, remove `mypy` cache:

```bash
rm -r .mypy_cache
```

### Testing stubs with `stubtest`

Run `bash ./scripts/stubtest.sh` to test that stubs and sources are in-line.

We have two special files to allow errors:
1. `scripts/stubtest/allowlist.txt` where we store things that we really don't care about: hacks, django internal utility modules, things that are handled by our plugin, things that are not representable by type system, etc
2. `scripts/stubtest/allowlist_todo.txt` where we store all errors there are right now. Basically, this is a TODO list: we need to work through this list and fix things (or move entries to real `allowlist.txt`). In the end, ideally we can remove this file

You might also want to disable `incremental` mode while working on `stubtest` changes.
This mode leads to several known problems (stubs do not show up or have strange errors).

**Important**: right now we only run `stubtest` on Python 3.11 (because it is the latest released version at the moment), any other versions might generate different outputs. Any work to create per-version allowlists is welcome.

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
If it does, please add the new generic class to the `_need_generic` list in the [`django_stubs_ext.patch` module](https://github.com/typeddjango/django-stubs/blob/master/django_stubs_ext/django_stubs_ext/patch.py).

## Private attributes

We only add hints for private attributes when it has some demonstrated real-world use case.
That means from a third-party package or some well described snippet for a project.
This rule helps us avoid tying in too closely to Django’s undocumented internals.
