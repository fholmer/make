import os
from functools import partial
from jinja2 import Template

from .parsers import ini_parser , json_parser

class Abort(ValueError):
    pass


class Invalid(ValueError):
    pass


class ParserNotFound(Exception):
    pass


Parsers = {
    "ini_parser": ini_parser.get_vars,
    "json_parser": json_parser.get_vars
}


def _render(kwargs, string):
    """
        Simple helperfunction to render a template.
        Plays nice with partial:

        .. code-block:: python

            render = partial(_render, variables)
            full_content = render(full_content)
    """
    return Template(string).render(kwargs)


def make_project(args):
    """
        * Fetches the source and target path.
        * Parses ``project.conf``
        * copy and transform files in source to target.
    """
    source = args.source.absolute()
    target = args.target.absolute()

    if not source.is_dir():
        raise Abort("Source %s does not exists" % source)

    if target.is_dir():
        raise Abort("Target %s already exists" % target)

    for parser in Parsers.values():
        try:
            variables = parser(args=args)
            if not variables is None:
                break
        except ParserNotFound:
            pass
    else:
        raise Abort("cannot parse source directory")

    render = partial(_render, variables)

    for action, root, fn in iter_filenames(source):
        if action == 1:
            _root = render(root)
            if _root and not contains_blanks(_root):
                target_path = target.joinpath(_root)
                if args.dry_run:
                    print("New path:", target_path)
                else:
                    os.makedirs(str(target_path))
        elif action == 2:
            _root = render(root)
            _fn = render(fn)
            # files in the root folder is ignored and files or folders with blank
            # name is also ignored
            if _fn and _root and not contains_blanks(_root):
                source_path = source.joinpath(root, fn)
                target_path = target.joinpath(_root, _fn)
                if args.dry_run:
                    print("New file:", str(target_path))
                else:
                    full_content = source_path.read_text()
                    full_content = render(full_content)
                    target_path.write_text(full_content)

_os_sep = os.path.sep
_os_sep_dbl = _os_sep + _os_sep

def contains_blanks(pth):
    return (_os_sep_dbl in pth) or pth.endswith(_os_sep)

def iter_filenames(source):
    """
        Walk through all files and yield one of the following:

        * (1, rootdir, dirname, None)
        * (2, rootdir, dirname, filename)

        Usage:

        .. code-block:: python

            for action, root, dn, fn in iter_filenames(some_dir):
                if action == 1:
                    print("I am {root}/{dn}, the directory)
                elif action == 2:
                    print("I am not")
    """

    root_index = len(str(source)) + 1
    for full_root, _dirs, files in os.walk(str(source)):
        root = full_root[root_index:]

        yield 1, root, None
        for fn in files:
            yield 2, root, fn
