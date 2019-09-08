import argparse
import time
import pytest
import pathlib
from unittest.mock import Mock, patch
from make.make_project import make_project
from make import errors
from make.make_project.data_medium.local import Local

def test__render_simple():
    assert "one:1" == make_project._render({"one":"1"}, "one:{{ one }}")


def test__render_extensions():
    assert time.strftime("%Y") == make_project._render({}, "{% now 'local', '%Y' %}")


def test_make_project_file_not_exists():
    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source="src", target="dst", zip=False, dry_run=False)
        )

    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source=".", target=".", zip=False, dry_run=False)
        )

    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source=".", target="dst", zip=False, dry_run=False)
        )


@patch.object(make_project, "get_target_medium")
@patch.object(make_project, "get_source_medium")
@patch.object(make_project, "create_files")
def test_make_project_file_exists(create_files, get_source_medium, get_target_medium):
    source_medium = Mock()
    target_medium = Mock()
    get_source_medium.return_value = source_medium
    get_target_medium.return_value = target_medium

    def check_parser_callback(source_medium, dry_run):
        assert source_medium is source_medium
        return {"proj":{"test":1}}

    with patch.dict(make_project.Parsers, {"parser":check_parser_callback}):

        make_project.make_project(
            args=argparse.Namespace(source="src", target="dst", dry_run=False)
        )

        create_files.assert_called_once_with(source_medium, target_medium, {"proj":{"test":1}})


def test_create_dirs():
    source_medium = Mock()
    target_medium = Mock()

    source_medium.root = pathlib.Path("src")
    target_medium.root = pathlib.Path("dst")

    target_medium.joinpath = Local.joinpath
    target_medium.contains_blanks = Local.contains_blanks

    variables = {"dir":{"name":"en"}}
    dirs = [[(1, "", None), (1, "{{dir.name}}", None)]]
    source_medium.iter_filenames.side_effect = dirs

    make_project.create_files(source_medium, target_medium, variables)

    target_medium.mkdir.assert_called_once_with(target_medium.root.joinpath("en"))

def test_create_files():
    source_medium = Mock()
    target_medium = Mock()

    source_medium.root = pathlib.Path("src")
    target_medium.root = pathlib.Path("dst")

    source_medium.read_text.return_value = "{{ file.content }}"

    target_medium.joinpath = Local.joinpath
    target_medium.contains_blanks = Local.contains_blanks

    variables = {"file":{"name":"fn", "content":"stuff"}}

    dirs = [[(2, "", ""), (2, "en", ""), (2, "en", "{{file.name}}")]]

    source_medium.iter_filenames.side_effect = dirs

    make_project.create_files(source_medium, target_medium, variables)

    source_medium.read_text.assert_called_once()
    _dst = target_medium.root.joinpath("en", "fn")
    target_medium.write_text.assert_called_once_with(_dst, "stuff")

def test_setup():

    subparser = Mock()
    subparser.add_parser.return_value = subparser

    make_project.setup(subparser)

    subparser.set_defaults.assert_called_once_with(func=make_project.make_project)
