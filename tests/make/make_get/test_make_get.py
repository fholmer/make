import argparse
import pathlib
from unittest.mock import Mock, patch

import pytest

from make import errors
from make.make_get import make_get


@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_make_get(urlretrive):
    make_get.make_get(args=argparse.Namespace(source="http://src", target="dst"))
    urlretrive.assert_called_once_with(
        "http://src", str(pathlib.Path("dst").absolute())
    )


@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_abort(urlretrive):
    with pytest.raises(errors.Abort):
        make_get.retrive_from_url("", "dst", "")


@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url(urlretrive):
    make_get.retrive_from_url("http://src", "dst", "")
    urlretrive.assert_called_once_with(
        "http://src", str(pathlib.Path("dst").absolute())
    )


@patch.object(make_get, "abs_from_url")
@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_github(urlretrive, abs_from_url):
    abs_from_url.return_value = fake_path("/test/test", "test")
    make_get.retrive_from_url("gh:fholmer/make", "", "")
    urlretrive.assert_called_once_with(
        "https://github.com/fholmer/make/archive/master.zip", "/test/test"
    )


@patch.object(make_get, "abs_from_url")
@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_gitlab(urlretrive, abs_from_url):
    abs_from_url.return_value = fake_path("/test/test", "test")
    make_get.retrive_from_url("gl:fholmer/make", "", "")
    urlretrive.assert_called_once_with(
        "https://gitlab.com/fholmer/make/-/archive/master/make-master.zip", "/test/test"
    )


@patch.object(make_get, "abs_from_url")
@patch("make.make_get.make_get.urlretrieve", return_value=Mock())
def test_retrive_from_url_gitlab_subdir(urlretrive, abs_from_url):
    abs_from_url.return_value = fake_path("/test/test", "test")
    make_get.retrive_from_url("gl:fholmer/make", "", "tests/make/make_project")
    urlretrive.assert_called_once_with(
        "https://gitlab.com/fholmer/make/-/archive/master/make-master.zip?path=tests%2Fmake%2Fmake_project",
        "/test/test",
    )


def test_setup():

    subparser = Mock()
    subparser.add_parser.return_value = subparser
    make_get.setup(subparser)
    subparser.set_defaults.assert_called_once_with(func=make_get.make_get)


def fake_path(path, name):
    pth = Mock()
    pth.name = name
    pth.__str__ = Mock(return_value=path)
    pth.exists.return_value = False
    return pth
