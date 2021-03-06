import pathlib
from functools import namedtuple
from unittest.mock import Mock, patch

import pytest

from make import errors
from make.make_project.data_medium.zipsource import LocalTargetAndZipSource, make_zipobj


@pytest.fixture
def zipsource():
    Fo = namedtuple("Fo", ("filename", "is_dir"))
    zipsource = LocalTargetAndZipSource("", "")
    zipsource.zip = Mock()
    zipsource.zip.filelist = [
        Fo("src/", lambda: True),
        Fo("src/en/", lambda: True),
        Fo("src/en/to", lambda: False),
        Fo("src/en/tre", lambda: False),
    ]

    def namelist():
        for i in ("src/", "src/en/", "src/en/to", "src/en/tre"):
            yield i

    zipsource.zip.namelist = namelist
    zipsource.zip.read.return_value = b"data"
    return zipsource


def test_iter_filenames(zipsource):
    walker = zipsource.iter_filenames(pathlib.PurePosixPath("src"))
    assert (1, "", None) == next(walker)
    assert (1, "en", None) == next(walker)
    assert (2, "en", "to") == next(walker)
    assert (2, "en", "tre") == next(walker)
    with pytest.raises(StopIteration):
        next(walker)


def test_exists(zipsource):
    assert zipsource.exists(pathlib.PurePosixPath("src/"))
    assert zipsource.exists(pathlib.PurePosixPath("src/en/to"))
    assert not zipsource.exists(pathlib.PurePosixPath("/src/no"))


def test_read_text(zipsource):
    res = zipsource.read_text(pathlib.PurePosixPath("to"))
    assert res == "data"


def test_read_bytes(zipsource):
    res = zipsource.read_bytes(pathlib.PurePosixPath("to"))
    assert res == b"data"


def test_ensure_source_root(zipsource):
    zipsource.root = pathlib.PurePosixPath("src/")
    zipsource.ensure_source_root()

    zipsource.root = pathlib.PurePosixPath("dst/")
    with pytest.raises(errors.Abort):
        zipsource.ensure_source_root()


def test_ensure_target_root(zipsource):
    zipsource.root = pathlib.PurePosixPath("src/")
    with pytest.raises(errors.Abort):
        zipsource.ensure_target_root()

    zipsource.root = pathlib.PurePosixPath("dst/")
    zipsource.ensure_target_root()


def test_ensure_target_exists(zipsource):
    with pytest.raises(errors.Abort):
        zipsource.ensure_target(pathlib.PurePosixPath("src/en/to"))


def test_ensure_target_not_exists(zipsource):
    zipsource.ensure_target(pathlib.PurePosixPath("src/no"))
