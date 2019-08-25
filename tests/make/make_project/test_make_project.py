import argparse
import pathlib
import time
import os
import posixpath
import ntpath
import pytest
from unittest.mock import Mock, patch
from make.make_project import make_project
from make import errors

_sep = os.path.sep

def test__render_simple():
    assert "one:1" == make_project._render({"one":"1"}, "one:{{ one }}")

def test__render_extensions():
    assert time.strftime("%Y") == make_project._render({}, "{% now 'local', '%Y' %}")

def test_contain_blanks():
    assert make_project.contains_blanks("root{0}".format(_sep))
    assert make_project.contains_blanks("root{0}{0}dir".format(_sep))
    assert make_project.contains_blanks("root{0}dir{0}".format(_sep))
    assert not make_project.contains_blanks("root{0}dir".format(_sep))

    make_project._os_sep = posixpath.sep
    make_project._os_sep_dbl = posixpath.sep + posixpath.sep
    assert make_project.contains_blanks("root/")
    assert make_project.contains_blanks("root//dir")
    assert make_project.contains_blanks("root/dir/")
    assert not make_project.contains_blanks("root/dir")

    make_project._os_sep = ntpath.sep
    make_project._os_sep_dbl = ntpath.sep + ntpath.sep
    assert make_project.contains_blanks("root\\")
    assert make_project.contains_blanks("root\\\\dir")
    assert make_project.contains_blanks("root\\dir\\")
    assert not make_project.contains_blanks("root/dir")

@patch(
    'os.walk',
     side_effect=[[
         ("src", ["en"], []),
         ("src/en", [], ["to", "tre"]),
     ]]
)
def test_iter_filenames(walk):
    walker = make_project.iter_filenames("src")
    assert (1, "", None) == next(walker)
    assert (1, "en", None) == next(walker)
    assert (2, "en", "to") == next(walker)
    assert (2, "en", "tre") == next(walker)
    with pytest.raises(StopIteration):
         next(walker)

def test_make_project_file_not_exists():
    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source="src", target="dst")
        )

    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source=".", target=".")
        )

    with pytest.raises(errors.Abort):
        make_project.Parsers = {}
        make_project.make_project(
            args=argparse.Namespace(source=".", target="dst")
        )


@patch.object(make_project, "create_files")
def test_make_project_file_exists(create_files):

    path = Mock()
    path.absolute.return_value = path
    path.is_dir.side_effect = [True, False]

    def check_parser_callback(args):
        assert isinstance(args, argparse.Namespace) 
        return {"proj":{"test":1}}

    with patch.dict(make_project.Parsers, {"parser":check_parser_callback}):

        with patch("pathlib.Path", return_value=path):

            #make_project.Parsers = {"parser":check_parser_callback}
            make_project.make_project(
                args=argparse.Namespace(source="src", target="dst", dry_run=False)
            )

            assert path.absolute.call_count == 2
            create_files.assert_called_once_with(path, path, False, {"proj":{"test":1}})


def test_create_dirs():
    source = Mock()
    target = Mock()
    target_path = Mock()
    target.joinpath.return_value = target_path

    variables = {"dir":{"name":"en"}}

    dirs = [[(1, "", None), (1, "{{dir.name}}", None)]]

    with patch.object(make_project, "iter_filenames", side_effect=dirs):
        make_project.create_files(source, target, False, variables)

        target.joinpath.assert_called_once_with("en")
        target_path.mkdir.assert_called_once()

def test_create_files():
    source = Mock()
    source_path = Mock()
    target = Mock()
    target_path = Mock()

    source.joinpath.return_value = source_path
    target.joinpath.return_value = target_path

    source_path.read_text.return_value = "{{ file.content }}"

    variables = {"file":{"name":"fn", "content":"stuff"}}

    dirs = [[(2, "", ""), (2, "en", ""), (2, "en", "{{file.name}}")]]

    with patch.object(make_project, "iter_filenames", side_effect=dirs):
        make_project.create_files(source, target, False, variables)

        target.joinpath.assert_called_once_with("en", "fn")
        source_path.read_text.assert_called_once()
        target_path.write_text.assert_called_once_with("stuff")
