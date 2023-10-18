#!/usr/bin/env python
from distutils.core import setup

from setuptools import find_packages

with open("README.md") as f:
    readme = f.read()

dependencies = [
    "django",
    "typing-extensions",
]

# NB! For clarity, keep version major.minor.patch in sync with django-stubs.
# It's fine to skip django-stubs-ext releases, but when doing a release, update this to newest django-stubs version.
setup(
    name="django-stubs-ext",
    version="4.2.5",
    description="Monkey-patching and extensions for django-stubs",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=["LICENSE.md"],
    url="https://github.com/typeddjango/django-stubs",
    author="Simula Proxy",
    author_email="3nki.nam.shub@gmail.com",
    maintainer="Marti Raudsepp",
    maintainer_email="marti@juffo.org",
    py_modules=[],
    python_requires=">=3.8",
    install_requires=dependencies,
    packages=["django_stubs_ext", *find_packages(exclude=["scripts"])],
    package_data={"django_stubs_ext": ["py.typed"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
    ],
    project_urls={
        "Release notes": "https://github.com/typeddjango/django-stubs/releases",
    },
)
