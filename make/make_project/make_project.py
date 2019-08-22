import json
import os
from configparser import ConfigParser
from functools import partial

from jinja2 import Template


class Abort(ValueError):
    pass


class Invalid(ValueError):
    pass


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

    variables = get_vars(args)

    render = partial(_render, variables)

    for a, root, fn in iter_filenames(source):
        if a == 1:
            _root = render(root)
            if _root:
                target_path = str(target.joinpath(_root))
                if args.dry_run:
                    print("New path:", target_path)
                else:
                    os.makedirs(target_path)
        elif a == 2:
            _root = render(root)
            _fn = render(fn)
            if _fn and _root:
                source_path = source.joinpath(root, fn)
                target_path = target.joinpath(_root, _fn)
                if args.dry_run:
                    print("New file:", str(target_path))
                else:
                    full_content = source_path.read_text()
                    full_content = render(full_content)
                    target_path.write_text(full_content)


def iter_filenames(source):
    """
        Walk through all files and yield one of the following:

        * (1, dirname, None)
        * (2, dirname, filename)

        Usage:

        .. code-block:: python

            for action, root, fn in iter_filenames(some_dir):
                if action == 1:
                    print("I am {root}, the directory)
                elif action == 2:
                    print("I am not")
    """

    root_index = len(str(source)) + 1
    for full_root, _dirs, files in os.walk(str(source)):
        root = full_root[root_index:]

        yield 1, root, None
        for fn in files:
            yield 2, root, fn


def get_vars(args, interactive=True):
    """
        Parse given file and copy the content to a dict of dicts.

        Also, the values are rendered with jinja2 template.

    """

    project_conf = args.source.absolute().joinpath("project.conf")
    if not project_conf.is_file():
        raise Abort("Config %s does not exists" % project_conf)

    config = ConfigParser()

    # This trick allows the option key to remain case-sensitive
    config.optionxform = str
    config.read(str(project_conf), encoding="utf8")

    variables = {}

    for section in config.sections():
        section_dict = dict(config[section])
        section_kwargs = {section: section_dict}
        variables[section] = {}

        if args.dry_run:
            print("Section:", section, project_conf)

        for key, val in section_dict.items():
            _val = Template(val).render(**section_kwargs)
            if interactive:
                _val = question(key, _val)
            if args.dry_run:
                print("Choice: ", key, "=", _val)

            variables[section][key] = _val

    return variables


def question(question, defaultvalue):

    if defaultvalue.startswith("json::"):
        _json_stuff = json.loads(defaultvalue[6:])

        if isinstance(_json_stuff, list):
            return question_from_list(question, _json_stuff)
        elif isinstance(_json_stuff, str):
            return question_from_string(question, _json_stuff)
        else:
            raise NotImplementedError
    else:
        return question_from_string(question, defaultvalue)


def question_from_string(quest, ion):
    reply = input("{}? [{}]: ".format(quest, ion))
    if reply:
        return reply
    return ion


def question_from_list(question, choices):
    size = len(choices)
    names = "\n".join(["{}) {}".format(i + 1, e) for i, e in enumerate(choices)])
    numbers = "([1], {})".format(", ".join(map(str, range(2, size + 1))))

    res = input("Options:\n{}\nChoose an option {}: ".format(names, numbers))
    ires = int(res or 1)
    if 0 < ires <= size:
        return choices[ires - 1]
    else:
        raise Invalid("Invalid option")
