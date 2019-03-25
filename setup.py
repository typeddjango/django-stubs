import os
import sys
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


with open('README.md', 'r') as f:
    readme = f.read()

dependencies = [
    'mypy>=0.670',
    'typing-extensions'
]
if sys.version_info[:2] < (3, 7):
    # dataclasses port for 3.6
    dependencies += ['dataclasses']

setup(
    name="django-stubs",
    version="0.10.1",
    description='Django mypy stubs',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    url="https://github.com/mkurnikov/django-stubs",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    py_modules=[],
    python_requires='>=3',
    install_requires=dependencies,
    packages=['django-stubs', *find_packages()],
    package_data={'django-stubs': find_stub_files('django-stubs')},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
