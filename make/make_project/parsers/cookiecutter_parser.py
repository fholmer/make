import json
import pathlib

from ...errors import Invalid, ParserNotFound
from ...template import Template

from .json_parser import question, question_from_list, question_from_string

def get_vars(args, interactive=True):
    """
        Parse given file and copy the content to a dict of dicts.

        Also, the values are rendered with jinja2 template.

    """

    project_conf = pathlib.Path(args.source).absolute().joinpath("cookiecutter.json")
    if not project_conf.is_file():
        raise ParserNotFound("Config %s does not exists" % project_conf)

    variables = {}

    with open(str(project_conf), "r") as f:
        section_dict = json.load(f)

    if not isinstance(section_dict, dict):
        raise Invalid("root object have to be of type dict")

    variables["cookiecutter"] = section_dict

    for key, val in section_dict.items():
        if isinstance(val, str):
            val = Template(val).render(variables)
        if interactive:
            val = question(key, val)
        if args.dry_run:
            print("Choice: ", key, "=", repr(val))

        section_dict[key] = val

    return variables
