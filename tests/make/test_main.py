import argparse
from unittest.mock import Mock, patch
from make import __main__

@patch(
    'argparse.ArgumentParser.parse_args',
     return_value=argparse.Namespace(conf_type="project")
)
def test_conf_type_project(parse_args):
    __main__.ConfTypes = {"project":Mock()}
    __main__.main()
    __main__.ConfTypes['project'].assert_called_once_with(args=parse_args())

@patch(
    'argparse.ArgumentParser.parse_args',
     return_value=argparse.Namespace(conf_type="get")
)
def test_conf_type_get(parse_args):
    __main__.ConfTypes = {"get":Mock()}
    __main__.main()
    __main__.ConfTypes['get'].assert_called_once_with(args=parse_args())

