import argparse
import pathlib
from unittest.mock import Mock, patch
import pytest

from make.make_get import make_get
from make import errors

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_make_get(urlretrive):
    make_get.make_get(args=argparse.Namespace(source="http://src", target="dst"))
    urlretrive.assert_called_once_with("http://src", pathlib.Path("dst").absolute())

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_abort(urlretrive):
    with pytest.raises(errors.Abort):
        make_get.retrive_from_url("", "dst", "")

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url(urlretrive):
    make_get.retrive_from_url("http://src", "dst", "")
    urlretrive.assert_called_once_with("http://src", pathlib.Path("dst").absolute())

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_github(urlretrive):
    make_get.retrive_from_url("gh:fholmer/make", "", "")
    urlretrive.assert_called_once_with(
        "https://github.com/fholmer/make/archive/master.zip",
        pathlib.Path("master.zip").absolute()
    )

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_github(urlretrive):
    make_get.retrive_from_url("gl:fholmer/make", "", "")
    urlretrive.assert_called_once_with(
        "https://gitlab.com/fholmer/make/-/archive/master/make-master.zip",
        pathlib.Path("make-master.zip").absolute()
    )

@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_github(urlretrive):
    make_get.retrive_from_url("gl:fholmer/make", "", "tests/make/make_project")
    urlretrive.assert_called_once_with(
        "https://gitlab.com/fholmer/make/-/archive/master/make-master.zip?path=tests%2Fmake%2Fmake_project",
        pathlib.Path("make-master.zip").absolute()
    )

def test_setup():

    subparser = Mock()
    subparser.add_parser.return_value = subparser

    make_get.setup(subparser)

    subparser.set_defaults.assert_called_once_with(func=make_get.make_get)
