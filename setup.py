#!/usr/bin/env python
import os
from typing import List

from setuptools import find_packages, setup


def find_stub_files(name: str) -> List[str]:
    result = []
    for root, _dirs, files in os.walk(name):
        for file in files:
            if file.endswith(".pyi"):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


with open("README.md") as f:
    readme = f.read()

dependencies = [
    "mypy>=1.0.0",
    "django",
    "django-stubs-ext>=4.2.5",
    "tomli; python_version < '3.11'",
    # Types:
    "typing-extensions",
    "types-pytz",
    "types-PyYAML",
]

# Keep compatible-mypy major.minor version pinned to what we use in CI (requirements.txt)
extras_require = {
    "compatible-mypy": ["mypy~=1.6.0"],
}

setup(
    name="django-stubs",
    version="4.2.5",
    description="Mypy stubs for Django",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    license_files=["LICENSE.md"],
    url="https://github.com/typeddjango/django-stubs",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    maintainer="Marti Raudsepp",
    maintainer_email="marti@juffo.org",
    py_modules=[],
    python_requires=">=3.8",
    install_requires=dependencies,
    extras_require=extras_require,
    packages=["django-stubs", *find_packages(exclude=["scripts"])],
    package_data={
        "django-stubs": find_stub_files("django-stubs"),
        "mypy_django_plugin": ["py.typed"],
    },
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
