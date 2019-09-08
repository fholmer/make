import pathlib
from unittest.mock import patch

import pytest

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
