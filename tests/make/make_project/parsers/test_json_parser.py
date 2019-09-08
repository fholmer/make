import argparse
from unittest.mock import Mock, mock_open, patch

from make.make_project.parsers import json_parser

JSON_STR = """{
    "project": {
        "name": "A-Project-Name",
        "package": "{{ project.name.lower().replace('-', '_') }}"
    }
}
"""


def test_get_vars():

    source_medium = Mock()
    source_medium.root = "/"
    source_medium.joinpath.return_value = "/project.json"
    source_medium.exists.return_value = True
    source_medium.read_text.return_value = JSON_STR

    variables = json_parser.get_vars(source_medium, False, interactive=False)

    source_medium.joinpath.assert_called_once_with("/", "project.json")
    source_medium.exists.assert_called_once()
    source_medium.read_text.assert_called_once()

    assert isinstance(variables, dict)
    assert variables == {
        "project": {"name": "A-Project-Name", "package": "a_project_name"}
    }
