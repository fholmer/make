from argparse import ArgumentParser

from .make_project.make_project import Abort, Invalid, make_project
from .make_get.make_get import make_get

ConfTypes = {
    "project": make_project,
    "get": make_get
}


def main():
    """
        Main entrypoint.

        .. code-block:: console

            usage: python -m make [-h] [--dry-run] conf_type source [target]

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
    global_parser.add_argument("source", type=str, help="source dir")
    global_parser.add_argument("target", type=str, nargs='?', default=".", help="target dir")
    global_parser.add_argument("--dry-run", action="store_true", help="test run")
    args = global_parser.parse_args()

    if args.conf_type and args.conf_type in ConfTypes:
        try:
            ConfTypes[args.conf_type](args=args)
        except Invalid as error:
            print("{}".format(error))
        except Abort as error:
            print("{}".format(error))
            global_parser.print_usage()
        except KeyboardInterrupt:
            print("Aborted by user")
    else:
        global_parser.print_help()


if __name__ == "__main__":
    main()
