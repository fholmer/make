Make
====

* Source Code: https://bitbucket.org/fholmer/make
* PyPI: https://pypi.org/project/make/
* License: BSD License

Summary
-------

Create project layout from jinja2 templates.

Installation
------------

.. code-block:: console

    $ pip install make

Usage
-----

Download and unpack a template:

.. code-block:: console

    $ python -m make get source-url target-path
    $ python -m zipfile -e target-path .

Create a new project based on the downloaded template:

.. code-block:: console

    $ python -m make project source-path target-path

Example:

Download a project template.
*We will use a popular cookiecutter template in this example*:

.. code-block:: console

    python -m make get https://github.com/kragniz/cookiecutter-pypackage-minimal/archive/master.zip pypackage.zip
    python -m zipfile -e pypackage.zip .

Create a new project:

.. code-block:: console

    python -m make project cookiecutter-pypackage-minimal-master New-Project



How to make a project template
------------------------------

The ``source-path`` have to contain a file named ``project.conf`` or
``project.json``.  Choose the format you prefer.

Format of ``project.conf``:

.. code-block:: ini

    [project]
    name = App
    package = {{project.name.lower().replace(' ','_').replace('-', '_')}}
    include_tests = json::["none", "pytest"]
    include_docs = json::["none", "sphinx", "mkdocs"]

    # this is a comment.
    # section or keys starting with _ is non-interactive variables

    _test_dir = {{ 'tests' if project.include_tests != 'none' else '' }}

    [_docs]
    dir=
        {%%- if project.include_docs == 'sphinx' -%%}
        docs
        {%%- elif project.include_docs == 'mkdocs' -%%}
        docz
        {%%- else -%%}
        {%%- endif -%%}

The ini-format allows for multi line values, but ``%`` have to be escaped.
Comments is allowed. Use the special prefix ``json::`` to serialize subsequent
text as json.

Format of ``project.json``:

.. code-block:: json

    {
        "project": {

            "name": "App",
            "package": "{{project.name.lower().replace(' ','_').replace('-', '_')}}",
            "include_tests": ["none", "pytest"],
            "include_docs": ["none", "sphinx", "mkdocs"],
            "_test_dir": "{{ 'tests' if project.include_tests != 'none' else '' }}"
        },
        "_docs": {
            "dir": "{%- if project.include_docs == 'sphinx' -%}\ndocs\n{%- elif project.include_docs == 'mkdocs' -%}\ndocz\n{%- else -%}\n{%- endif -%}"
        }
    }

The json-format do not have multi line but you can use multiple ``\n`` in one
line.

The source directory could be something like this:

.. code-block:: text

    /My-Project-Template
      /{{project.name}}
        /{{_docs.dir}}
          conf.py
        /{{project._test_dir}}
        /{{project.package}}
          __init__.py
        setup.py
        LICENSE
        README.rst
      project.conf

``{{project.name}}/setup.py`` may look something like this:

.. code-block:: python

        from setuptools import setup, find_packages
        from {{ project.package }} import __version__ as app_version

        setup(
            name="{{ project.name }}",
            version=app_version,
            packages=find_packages(include=['{{ project.package }}*']),
        )
