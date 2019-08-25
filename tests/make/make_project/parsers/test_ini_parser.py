import argparse
from configparser import ConfigParser
from unittest.mock import Mock, patch
from make.make_project.parsers import ini_parser

INI_STR = """[project]
name = A-Project-Name
package = {{ project.name.lower().replace('-', '_') }}
"""

def test_get_vars():

    path = Mock()
    path.absolute.return_value = path
    path.joinpath.return_value = path
    path.is_file.return_value = True

    with patch("pathlib.Path", return_value=path):

        conf = ConfigParser()
        conf.read_string(INI_STR)

        with patch.object(ini_parser, "ConfigParser", return_value=conf):

            args = argparse.Namespace(source=".", dry_run=False)
            variables = ini_parser.get_vars(args, interactive=False)

            path.absolute.assert_called_once_with()
            path.joinpath.assert_called_once_with("project.conf")
            path.is_file.assert_called_once_with()

            assert isinstance(variables, dict)
            assert variables == {
                "project": {
                    "name": "A-Project-Name",
                    "package": "a_project_name"
                }
            }
