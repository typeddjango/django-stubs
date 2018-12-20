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
        'mypy @ git+https://github.com/python/mypy.git#egg=mypy-0.660+dev.01c268644d1d22506442df4e21b39c04710b7e8b'
    ],
    packages=['mypy_django_plugin']
)
