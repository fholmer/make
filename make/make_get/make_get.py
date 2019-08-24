from pathlib import Path
from urllib.request import urlretrieve
from ..errors import Abort

def make_get(args):
    """
        Download ``source`` and store it to disk as ``target``
    """
    source = str(args.source)
    target = Path(args.target).absolute()
    if target.exists():
        raise Abort("target file: {} already exists".format(target))

    print("Download: ", source)
    print("Into    : ", target)
    urlretrieve(source, target)