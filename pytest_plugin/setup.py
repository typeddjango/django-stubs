import sys

from setuptools import setup

# with open('README.md', 'r') as f:
#     readme = f.read()

dependencies = [
    # 'pytest-mypy-plugins',
    # 'mypy',
    # 'decorator',
    # 'capturer'
]
# if sys.version_info[:2] < (3, 7):
#     # dataclasses port for 3.6
#     dependencies += ['dataclasses']

setup(
    name='pytest-django-stubs-newsemanal',
    version='0.4.0',
    # description='pytest plugin for writing tests for mypy plugins',
    # long_description=readme,
    # long_description_content_type='text/markdown',
    license='MIT',
    url="https://github.com/mkurnikov/pytest-mypy-plugins",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    # packages=['pytest_plugin'],
    # the following makes a plugin available to pytest
    entry_points={
        'pytest11': [
            'pytest-django-stubs-newsemanal = pytest_plugin.collect'
        ]
    },
    install_requires=dependencies,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
