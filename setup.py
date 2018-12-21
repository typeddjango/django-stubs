from distutils.core import setup

setup(
    name="django-stubs",
    url="https://github.com/mkurnikov/django-stubs.git",
    author="Maksim Kurnikov",
    author_email="maxim.kurnikov@gmail.com",
    version="0.1.0",
    license='BSD',
    install_requires=[
        'Django',
        'mypy @ git+https://github.com/python/mypy.git#egg=mypy-0.660+dev.a7296c4595350768ec8ecf145c23a76b6c98e8e6'
    ],
    packages=['mypy_django_plugin']
)
