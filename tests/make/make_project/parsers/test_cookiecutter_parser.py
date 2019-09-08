import argparse
from unittest.mock import Mock, patch, mock_open
from make.make_project.parsers import cookiecutter_parser

JSON_STR = """{
    "name": "A-Project-Name",
    "package": "{{ cookiecutter.name.lower().replace('-', '_') }}"
}
"""

def test_get_vars():

    source_medium = Mock()
    source_medium.root = "/"
    source_medium.joinpath.return_value = "/cookiecutter.json"
    source_medium.exists.return_value = True
    source_medium.read_text.return_value = JSON_STR

    variables = cookiecutter_parser.get_vars(source_medium, False, interactive=False)

    source_medium.joinpath.assert_called_once_with("/", "cookiecutter.json")
    source_medium.exists.assert_called_once()
    source_medium.read_text.assert_called_once()

    assert isinstance(variables, dict)
    assert variables == {
        "cookiecutter": {
            "name": "A-Project-Name",
            "package": "a_project_name"
        }
    }
