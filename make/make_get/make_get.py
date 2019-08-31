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

def setup(subparsers):
    parser = subparsers.add_parser('get', help='Download source and store as target')
    parser.add_argument("source", type=str, help="source URL")
    parser.add_argument("target", type=str, nargs='?', default=".", help="target dir")
    parser.set_defaults(func=make_get)
