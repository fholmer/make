import pathlib
from argparse import ArgumentParser

from .make_project.make_project import Abort, Invalid, make_project

ConfTypes = {"project": make_project}


def main():
    """
        Main entrypoint.

        .. code-block:: console

            usage: python -m make [-h] conf_type source target

            positional arguments:
            conf_type   configuration type
            source      source dir
            target      target dir

            optional arguments:
            -h, --help  show this help message and exit
            --dry-run   test run
    """

    global_parser = ArgumentParser(add_help=True)
    global_parser.add_argument("conf_type", type=str, help="configuration type")
    global_parser.add_argument("source", type=pathlib.Path, help="source dir")
    global_parser.add_argument("target", type=pathlib.Path, help="target dir")
    global_parser.add_argument("--dry-run", action="store_true", help="test run")
    args = global_parser.parse_args()

    conf_type = args.conf_type
    if args.conf_type and args.conf_type in ConfTypes:
        try:
            ConfTypes[args.conf_type](args=args)
        except Invalid as error:
            print("{}".format(error))
        except Abort as error:
            print("{}".format(error))
            global_parser.print_usage()
    else:
        global_parser.print_help()


if __name__ == "__main__":
    main()
