import argparse
import pathlib
from unittest.mock import Mock, patch
from make.make_get.make_get import make_get

@patch(
    'make.make_get.make_get.urlretrieve',
     return_value=Mock()
)
def test_make_get(urlretrive):
    make_get(args=argparse.Namespace(source="src", target="dst"))
    urlretrive.assert_called_once_with(
        "src",
        pathlib.Path("dst").absolute()
    )