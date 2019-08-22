import os
from jinja2 import Template
from functools import partial
from configparser import ConfigParser

def _render(kwargs, string):
    """
        Simple helperfunction to render a template.
        Plays nice with partial:

        .. code-block:: python

            render = partial(_render, variables)
            full_content = render(full_content)
    """
    return Template(string).render(**kwargs)

def make_project(args):
    """
        * Fetches the source and target path.
        * Parses ``project.conf``
        * copy and transform files in source to target.
    """
    source = args.source.expanduser().absolute()
    target = args.target.expanduser().absolute()

    if not source.is_dir():
        print("%s does not exists" % source)
        return

    if target.is_dir():
        print("%s already exists" % target)
        return

    project_conf = source.joinpath("project.conf")
    if not project_conf.is_file():
        print("%s does not exists" % project_conf)
        return

    variables = get_vars(project_conf)

    render = partial(_render, variables)

    for a, root, fn in iter_filenames(source):
        if a == 1:
            target_path = str(target.joinpath(render(root)))
            os.makedirs(target_path)
        elif a == 2:
            source_path = source.joinpath(root, fn)
            target_path = target.joinpath(render(root), render(fn))
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

def get_vars(project_conf):
    """
        Parse given file and copy the content to a dict of dicts.

        Also, the values are rendered with jinja2 template.

    """

    config = ConfigParser()

    #This trick allows the option key to remain case-sensitive
    config.optionxform = str
    config.read(project_conf, encoding="utf8")

    variables = {}

    for section in config.sections():
        section_dict = dict(config[section])
        section_kwargs = {section:section_dict}
        variables[section] = {}

        for key, val in section_dict.items():
            variables[section][key] = Template(val).render(**section_kwargs)

    return variables
