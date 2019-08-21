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

Download required packages:
    
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

from make import __version__ as app_version

here = path.abspath(path.dirname(__file__))

NAME = "make"
MAIN_PACKAGE = "make"


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    # default setuptools options:
    name=NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=app_version,

    description="Create project layout from jinja2 templates.",
    long_description=long_description,

    # The project's main homepage.
    url='https://bitbucket.org/fholmer/make',

    # Author details
    author="Frode Holmer",
    author_email='fholmer+netdef@gmail.com',

    # Choose your license
    license='GNU Lesser General Public License v3 or later',

    project_urls={
        "Source Code": "https://bitbucket.org/fholmer/make",
    },

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows'
    ],

    keywords='Networking Monitoring',

    packages=find_packages(include=['make*']),

    install_requires=[
        'Jinja2'
    ]
)
