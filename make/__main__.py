from argparse import ArgumentParser
import pathlib
from .make_project.make_project import make_project

ConfTypes = {
    'project': make_project
}

def main():
    global_parser = ArgumentParser(add_help=True)
    global_parser.add_argument('conf_type', type=str, help='configuration type')
    global_parser.add_argument('source', type=pathlib.Path, help='source dir')
    global_parser.add_argument('target', type=pathlib.Path, help='target dir')
    args = global_parser.parse_args()

    conf_type = args.conf_type
    if args.conf_type and args.conf_type in ConfTypes:
        ConfTypes[args.conf_type](args=args)
    else:
        global_parser.print_help()

if __name__ == '__main__':
    main()
