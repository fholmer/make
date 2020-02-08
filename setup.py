# -*- coding: utf-8 -*-
"""A setuptools based setup module.

Code style:
    python -m isort -rc make tests
    python -m black make tests

Build wheel:
    python setup.py bdist_wheel

Update requirements:
    python -m pip freeze -r requirements.txt > requirements.txt

Upload to pypi:
    python -m twine upload dist/*

"""

# To use a consistent encoding
from codecs import open
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

from make import __version__ as app_version

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="make",
    version=app_version,
    description="Create project layout from jinja2 templates.",
    long_description=long_description,
    keywords="make project template",
    url="https://github.com/fholmer/make",
    author="Frode Holmer",
    author_email="fholmer+make@gmail.com",
    license="BSD License",
    project_urls={"Source Code": "https://github.com/fholmer/make"},
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(include=["make*"]),
    install_requires=["Jinja2", "jinja2-time"],
)
