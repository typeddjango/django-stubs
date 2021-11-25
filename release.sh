#!/usr/bin/env bash
set -ex

if [[ -z $(git status -s) ]]
then
  if [[ "$VIRTUAL_ENV" != ""  ]]
  then
    pip install --upgrade setuptools wheel twine
    python setup.py sdist bdist_wheel
    twine upload dist/*
    rm -rf dist/ build/
  else
    echo "this script must be executed inside an active virtual env, aborting"
  fi
else
  echo "git working tree is not clean, aborting"
fi
