"""Setup file that prepares the package and installs it."""
# 3rd-party
from setuptools import find_packages
from setuptools import setup

setup(
    packages=find_packages(
        exclude=[
            'testapp',
            'testapp.tests',
        ],
    ),
    install_requires=[
        'requests==2.28.1',
        'django==3.2.15',
        'django-money==3.0.0',
    ],
)
