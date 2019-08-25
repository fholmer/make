import argparse
from unittest.mock import Mock, patch, mock_open
from make.make_project.parsers import json_parser

JSON_STR = """{
    "project": {
        "name": "A-Project-Name",
        "package": "{{ project.name.lower().replace('-', '_') }}"
    }
}
"""

def test_get_vars():

    path = Mock()
    path.absolute.return_value = path
    path.joinpath.return_value = path
    path.is_file.return_value = True

    with patch("pathlib.Path", return_value=path):

        with patch.object(json_parser, 'open', mock_open(read_data=JSON_STR)):

            args = argparse.Namespace(source=".", dry_run=False)
            variables = json_parser.get_vars(args, interactive=False)

            path.absolute.assert_called_once_with()
            path.joinpath.assert_called_once_with("project.json")
            path.is_file.assert_called_once_with()

            assert isinstance(variables, dict)
            assert variables == {
                "project": {
                    "name": "A-Project-Name",
                    "package": "a_project_name"
                }
            }
