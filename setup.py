import os
from distutils.core import setup

from setuptools import find_packages


def find_stub_files(name):
    result = []
    for root, dirs, files in os.walk(name):
        for file in files:
            if file.endswith('.pyi'):
                if os.path.sep in root:
                    sub_root = root.split(os.path.sep, 1)[-1]
                    file = os.path.join(sub_root, file)
                result.append(file)
    return result


setup(
    name="django-stubs",
    description='Django mypy stubs',
    version="0.2.0",
    license='BSD',
    url="https://github.com/mkurnikov/django-stubs.git",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    py_modules=[],
    python_requires='>=3',
    install_requires=[
        'Django',
        'mypy'
    ],
    packages=['django-stubs', *find_packages()],
    package_data={'django-stubs': find_stub_files('django-stubs')},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3'
    ]
)
