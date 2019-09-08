import ntpath
import os
import posixpath
from unittest.mock import patch

from make.make_project.data_medium.base import DataMediumBase

_sep = os.path.sep


def test_contain_blanks():
    assert DataMediumBase.contains_blanks("root{0}".format(_sep))
    assert DataMediumBase.contains_blanks("root{0}{0}dir".format(_sep))
    assert DataMediumBase.contains_blanks("root{0}dir{0}".format(_sep))
    assert not DataMediumBase.contains_blanks("root{0}dir".format(_sep))

    with patch.object(DataMediumBase, "os_sep", posixpath.sep):
        with patch.object(DataMediumBase, "os_sep_dbl", posixpath.sep + posixpath.sep):
            assert DataMediumBase.contains_blanks("root/")
            assert DataMediumBase.contains_blanks("root//dir")
            assert DataMediumBase.contains_blanks("root/dir/")
            assert not DataMediumBase.contains_blanks("root/dir")

    with patch.object(DataMediumBase, "os_sep", ntpath.sep):
        with patch.object(DataMediumBase, "os_sep_dbl", ntpath.sep + ntpath.sep):
            assert DataMediumBase.contains_blanks("root\\")
            assert DataMediumBase.contains_blanks("root\\\\dir")
            assert DataMediumBase.contains_blanks("root\\dir\\")
            assert not DataMediumBase.contains_blanks("root/dir")
