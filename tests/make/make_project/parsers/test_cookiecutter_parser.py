import argparse
from unittest.mock import Mock, patch, mock_open
from make.make_project.parsers import cookiecutter_parser

JSON_STR = """{
    "name": "A-Project-Name",
    "package": "{{ cookiecutter.name.lower().replace('-', '_') }}"
}
"""

def test_get_vars():

    path = Mock()
    path.absolute.return_value = path
    path.joinpath.return_value = path
    path.is_file.return_value = True

    with patch("pathlib.Path", return_value=path):

        with patch.object(cookiecutter_parser, 'open', mock_open(read_data=JSON_STR)):

            args = argparse.Namespace(source=".", dry_run=False)
            variables = cookiecutter_parser.get_vars(args, interactive=False)

            path.absolute.assert_called_once_with()
            path.joinpath.assert_called_once_with("cookiecutter.json")
            path.is_file.assert_called_once_with()

            assert isinstance(variables, dict)
            assert variables == {
                "cookiecutter": {
                    "name": "A-Project-Name",
                    "package": "a_project_name"
                }
            }
