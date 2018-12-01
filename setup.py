import os
from distutils.core import setup


def find_stubs(package):
    stubs = []
    for root, dirs, files in os.walk(package):
        for file in files:
            path = os.path.join(root, file).replace(package + os.sep, '', 1)
            stubs.append(path)
    return {package: stubs}


setup(
    name="django-stubs",
    url="https://github.com/mkurnikov/django-stubs.git",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    version="0.1.0",
    license='BSD',
    install_requires=[
        'Django>=2.1.1',
        'mypy'
    ],
    packages=['mypy_django_plugin'],
)
