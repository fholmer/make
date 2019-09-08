import argparse
from configparser import ConfigParser
from unittest.mock import Mock, patch

from make.make_project.parsers import ini_parser

INI_STR = """[project]
name = A-Project-Name
package = {{ project.name.lower().replace('-', '_') }}
"""


def test_get_vars():

    source_medium = Mock()
    source_medium.root = "/"
    source_medium.joinpath.return_value = "/cookiecutter.json"
    source_medium.exists.return_value = True
    source_medium.read_text.return_value = INI_STR

    variables = ini_parser.get_vars(source_medium, False, interactive=False)

    source_medium.joinpath.assert_called_once_with("/", "project.conf")
    source_medium.exists.assert_called_once()
    source_medium.read_text.assert_called_once()

    assert isinstance(variables, dict)
    assert variables == {
        "project": {"name": "A-Project-Name", "package": "a_project_name"}
    }
