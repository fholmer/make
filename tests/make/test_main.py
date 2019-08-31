import argparse
from unittest.mock import Mock, patch
from make import __main__

@patch('argparse.ArgumentParser.parse_args')
def test_func_none(parse_args):
    parse_args.return_value=argparse.Namespace(func=None)

    __main__.main()

    parse_args.assert_called_once_with()

@patch('argparse.ArgumentParser.parse_args')
def test_func_callback(parse_args):
    func = Mock()
    parse_args.return_value=argparse.Namespace(func=func)

    __main__.main()

    parse_args.assert_called_once_with()
    func.assert_called_once_with(args=parse_args())
