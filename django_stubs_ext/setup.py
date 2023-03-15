from distutils.core import setup

from setuptools import find_packages

with open("README.md") as f:
    readme = f.read()

dependencies = [
    "django",
    "typing-extensions",
]

setup(
    name="django-stubs-ext",
    version="0.8.0",
    description="Monkey-patching and extensions for django-stubs",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/typeddjango/django-stubs",
    author="Simula Proxy",
    author_email="3nki.nam.shub@gmail.com",
    maintainer="Marti Raudsepp",
    maintainer_email="marti@juffo.org",
    py_modules=[],
    python_requires=">=3.7",
    install_requires=dependencies,
    packages=["django_stubs_ext", *find_packages(exclude=["scripts"])],
    package_data={"django_stubs_ext": ["py.typed"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
    ],
    project_urls={
        "Release notes": "https://github.com/typeddjango/django-stubs/releases",
    },
)
