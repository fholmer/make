Make
====

* Source Code: https://bitbucket.org/fholmer/make
* PyPI: https://pypi.org/project/make/
* License: GNU Lesser General Public License v3 or later (LGPLv3+)

Summary
-------

Create project layout from jinja2 templates.

Installation
------------

.. code-block:: console

    $ pip install make

Usage
-----

.. code-block:: console

    $ python -m make project source-path target-path

The source path have to contain a file named ``project.conf``

The format of the file is more or less ini format:

.. code-block:: ini

    [general]
    project_name = My-Project
    package_name = {{ project.project_name.lower().replace(' ', '_').replace('-', '_') }}

Section names and key names can be anything. Usage in a python file:

``setup.py``:

.. code-block:: python

        from setuptools import setup, find_packages
        from {{ general.package_name }} import __version__ as app_version

        setup(
            name="{{ general.project_name }}",
            version=app_version,
            packages=find_packages(include=['{{ general.package_name }}*']),
        )
