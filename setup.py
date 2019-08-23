# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html


To build sdist:
    python3 setup.py sdist

To build wheel:
    install wheel:
      python3 -m pip install wheel
    build wheel:
      python3 setup.py bdist_wheel

Update requirements:
    python3 -m pip freeze -r requirements.txt > requirements.txt

Upload to pypi:
    python3 -m twine upload dist/*

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
    url="https://bitbucket.org/fholmer/make",
    author="Frode Holmer",
    author_email="fholmer+netdef@gmail.com",
    license="BSD License",
    project_urls={"Source Code": "https://bitbucket.org/fholmer/make"},
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
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages(include=["make*"]),
    install_requires=["Jinja2"],
)
