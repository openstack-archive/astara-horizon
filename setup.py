#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='akanda-rug-horizon',
    version='0.1',
    packages=find_packages("akanda"),
    package_dir={'': 'akanda'},
    install_requires=[
        'requests',
    ],
)
