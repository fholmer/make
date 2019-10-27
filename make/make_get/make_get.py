from pathlib import Path
from urllib.request import urlretrieve
from urllib import parse

from ..errors import Abort


def make_get(args):
    """
        Download ``source`` and store it to disk as ``target``
    """
    retrive_from_url(str(args.source), str(args.target), "")

def retrive_from_url(source, target, subpath):
    """
        Download ``source`` and store it to disk as ``target``
    """

    uri = parse.urlsplit(source)

    if uri.scheme in ("file", ""):
        raise Abort("URI not supported: {}".format(source))

    if uri.scheme == "gh":
        # https://github.com/fholmer/make/archive/master.zip
        uri = parse.SplitResult(
            "https",
            "github.com",
            "{}/archive/master.zip".format(uri.path),
            "",
            ""
        )
        source = uri.geturl()

    elif uri.scheme == "gl":
        # https://gitlab.com/fholmer/make/-/archive/master/make-master.zip
        # https://gitlab.com/fholmer/make/-/archive/master/make-master.zip?path=tests%2Fmake%2Fmake_project
        if subpath:
            subpath = parse.urlencode({"path":subpath})
        uri = parse.SplitResult(
            "https",
            "gitlab.com",
            "/{0[0]}/{0[1]}/-/archive/master/{0[1]}-master.zip".format(uri.path.split("/")),
            subpath,
            ""
        )
        source = uri.geturl()

    print(repr(target))
    if target:
        target = Path(target).absolute()
    else:
        target = Path(Path(uri.path).name).absolute()


    if target.exists():
        raise Abort("target file: {} already exists".format(target))

    print("Download: ", source)
    print("Into    : ", target)
    urlretrieve(source, target)
    return target


def setup(subparsers):
    parser = subparsers.add_parser("get", help="Download source and store as target")
    parser.add_argument("source", type=str, help="source URL")
    parser.add_argument("target", type=str, nargs="?", default="", help="target dir")
    parser.set_defaults(func=make_get)
