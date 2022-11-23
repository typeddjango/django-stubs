#!/usr/bin/env -S just --justfile

# Config
# =====================================================================

set dotenv-load := true
set shell := [ "bash", "-euo", "pipefail", "-c" ]

# these names are short because they will be used a lot
FROM := invocation_directory()
HERE := justfile_directory()
SELF := justfile()
SHELL := file_stem(`test -n "$0" && echo "$0" || status fish-path`)

# more explicit names are exported
export JUSTFILE := SELF
export JUSTFILE_DIR := HERE
export JUST_INVOCATION_DIR := FROM
export JUST_INVOCATION_SHELL := SHELL

# Handy bits
t := "true"
f := "false"

# Path of .env file (not configurable)
dotenv := HERE / ".env"
dotexample := HERE / ".env.example"

# The Python executable used to create the project virtualenv
srcpy := env_var_or_default("DJANGO_STUBS_PYTHON", "python3")

# The path at which to create the project virtualenv
venv_dir := env_var_or_default("DJANGO_STUBS_VENV", HERE / ".venv")
venv_bin := venv_dir / "bin"
venv_act := venv_bin / "activate" + if SHELL =~ '^(fi|c)sh$' { "." + SHELL } else { "" }

# The Python executable of the project virtualenv
pyexe := venv_bin / "python"

# The version of Django for which to test and build
export DJANGO_VERSION := env_var_or_default("DJANGO_VERSION", "3.2")

export PATH := venv_bin + ":" + env_var("PATH")


# Aliases
# =====================================================================

alias h := help
alias t := test
alias rm := clean
alias clear := clean


# Recipes
# =====================================================================

## General
## --------------------------------------------------------------------

# run this recipe if no arguments are given (by virtue of it being the *first* recipe)
@_default: ls

# list available recipes
@ls:
  "{{ SELF }}" --list --unsorted

# print help info & list available recipes
@help: && ls
  "{{ SELF }}" --help


## Development
## --------------------------------------------------------------------

# refresh setup, run checks & builds
full: clean setup lint test build

# remove development artifacts
clean: _clean-precommit _clean-setuptools _clean-project

# uninstall pre-commit hooks and clean up artifacts
_clean-precommit:
  -pre-commit uninstall
  -pre-commit clean
  -pre-commit gc

# run setuptools clean command, delete other artifacts
_clean-setuptools:
  -"{{ if path_exists(pyexe) == t { pyexe } else { srcpy } }}" setup.py clean --all
  -cd django_stubs_ext && "{{ if path_exists(pyexe) == t { pyexe } else { srcpy } }}" setup.py clean --all
  -rm -rf {.,django_stubs_ext}/*.egg-info
  -rm -rf {.,django_stubs_ext}/build
  -rm -rf {.,django_stubs_ext}/dist
  -rm -rf {.,django_stubs_ext}/django-stubs-*.*.?*

# remove all artifacts not removed by other cleaners
_clean-project:
  -rm -rf "{{ venv_dir }}"
  -rm -rf {.,django_stubs_ext}/.*cache
  @# Remove the dotenv file if it is no different from the example one.
  -! diff -q "{{ dotenv }}" "{{ dotexample }}" >/dev/null 2>&1 || rm "{{ dotenv }}"
  @# TODO: Consider deleting these safely by using a prompt & --noinput switch.
  @echo "Manually delete the following, if needed:"
  @printf -- "    %s\n" $(python scripts/paths.py)


# setup up project development environment
setup:
  @# @test ! -e "{{ pyexe }}" && "{{ SELF }}" _setup || "{{ SELF }}" _install
  @"{{ SELF }}" {{ if path_exists(pyexe) == f { "_setup" } else { "_install" } }}
  @echo "If needed, generate draft stubs by running 'just draft-stubs"

# create virtualenv, install requirements
_setup: && _install
  test -e "{{ dotenv }}" || cp "{{ dotexample }}" "{{ dotenv }}"
  test ! -e "{{ venv_dir }}" || rm -rf "{{ venv_dir }}"
  "{{ srcpy }}" -m venv "{{ venv_dir }}"

_install:
  "{{ pyexe }}" -m pip install -U pip setuptools wheel
  "{{ pyexe }}" -m pip install -r requirements.txt
  "{{ pyexe }}" -m pre_commit install --install-hooks

# generate new draft stub files
draft-stubs:
  "{{ pyexe }}" scripts/stubgen-django.py --django_version "$DJANGO_VERSION"


## Lint & Test
## --------------------------------------------------------------------

# run all linters & checkers
lint: lint-precommit lint-mypy

# run pre-commit hooks
lint-precommit *ARGS="--all-files":
  "{{ pyexe }}" -m pre_commit run {{ ARGS }}

# typecheck project w/ mypy
lint-mypy:
  @# see `.github/workflows/tests.yml:jobs.mypy-self-check.steps`
  "{{ pyexe }}" -m mypy --strict mypy_django_plugin
  "{{ pyexe }}" -m mypy --strict django_stubs_ext
  "{{ pyexe }}" -m mypy --strict scripts
  "{{ pyexe }}" -m mypy --cache-dir=/dev/null --no-incremental django-stubs

# run all tests
test: test-py test-dj

# run unit tests w/ pytest
test-py *ARGS:
  @# see `.github/workflows/tests.yml:jobs.test.steps`
  "{{ pyexe }}" -m pytest {{ ARGS }}

# typecheck Django tests w/ mypy using project stubs
test-dj:
  @# see `.github/workflows/tests.yml:jobs.typecheck.steps`
  "{{ pyexe }}" scripts/typecheck_tests.py --django_version "$DJANGO_VERSION"


## Build
## --------------------------------------------------------------------

# build project packages
build: build-pkg build-pkg-ext

# build django-stubs package
build-pkg:
  "{{ pyexe }}" -m pip install --upgrade setuptools wheel twine
  "{{ pyexe }}" setup.py check sdist bdist_wheel

# build django-stubs-ext package
build-pkg-ext:
  "{{ pyexe }}" -m pip install --upgrade setuptools wheel twine
  cd django_stubs_ext && "{{ pyexe }}" setup.py check sdist bdist_wheel


## Release
## --------------------------------------------------------------------

# build & release project packages
release: full release-pkg release-pkg-ext

# build & release django-stubs package
release-pkg:
  . "{{ venv_act }}" && ./scripts/release.sh

# build & release django-stubs-ext package
release-pkg-ext:
  cd django_stubs_ext && . "{{ venv_act }}" && ./release.sh
