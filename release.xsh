#!/usr/local/bin/xonsh

try:
    pip install wheel
    python setup.py sdist bdist_wheel --universal
    twine upload dist/*

finally:
    rm -rf dist/ build/