from setuptools import setup

dependencies = [
    'pytest-mypy-plugins',
]

setup(
    name='pytest-django-stubs-newsemanal',
    version='0.4.0',
    license='MIT',
    url="https://github.com/mkurnikov/pytest-mypy-plugins",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
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
