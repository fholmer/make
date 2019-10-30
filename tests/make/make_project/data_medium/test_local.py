import pathlib
from unittest.mock import Mock, patch

import pytest

from make import errors
from make.make_project.data_medium.local import Local


@patch("os.walk", side_effect=[[("src", ["en"], []), ("src/en", [], ["to", "tre"])]])
def test_iter_filenames(walk):
    walker = Local.iter_filenames(pathlib.Path("src"))
    assert (1, "", None) == next(walker)
    assert (1, "en", None) == next(walker)
    assert (2, "en", "to") == next(walker)
    assert (2, "en", "tre") == next(walker)
    with pytest.raises(StopIteration):
        next(walker)


def test_local():
    local = Local("usr")
    assert isinstance(local.root, pathlib.Path)


def test_exists():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.exists("")

    pth = Mock()
    local.exists(pth)
    pth.exists.assert_called_once()


def test_joinpath():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.joinpath("usr1", "usr2", "usr3")

    pth = Mock()
    local.joinpath(pth, "usr2", "usr3")
    pth.joinpath.assert_called_once_with("usr2", "usr3")


def test_mkdir():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.mkdir("usr1")

    pth = Mock()
    local.mkdir(pth)
    pth.mkdir.assert_called_once_with(parents=True)


def test_write_text():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.write_text("usr1", "data")

    pth = Mock()
    local.write_text(pth, "data")
    pth.write_text.assert_called_once_with("data")


def test_write_bytes():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.write_bytes("usr1", b"data")

    pth = Mock()
    local.write_bytes(pth, b"data")
    pth.write_bytes.assert_called_once_with(b"data")


def test_read_text():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.read_text("usr1")

    pth = Mock()
    pth.read_text.return_value = "data"
    assert local.read_text(pth) == "data"


def test_read_bytes():
    local = Local("usr")

    with pytest.raises(AttributeError):
        local.read_bytes("usr1")

    pth = Mock()
    pth.read_bytes.return_value = b"data"
    assert local.read_bytes(pth) == b"data"


@patch("pathlib.Path", return_value=Mock())
def test_ensure_source(path):
    path.return_value = path
    path.absolute.return_value = path
    path.is_dir.side_effect = [True, False]

    local = Local("usr")
    path.assert_called_once()

    local.ensure_source()
    path.is_dir.assert_called_once()

    with pytest.raises(errors.Abort):
        local.ensure_source()


@patch("pathlib.Path", return_value=Mock())
def test_ensure_target(path):
    path.return_value = path
    path.absolute.return_value = path
    path.is_dir.side_effect = [False, True]

    local = Local("usr")
    path.assert_called_once()

    local.ensure_target()
    path.is_dir.assert_called_once()

    with pytest.raises(errors.Abort):
        local.ensure_target()
