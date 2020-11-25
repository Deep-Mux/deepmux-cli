import sys
import argparse

from deepmux.config import config
from deepmux.cmd import env, list_, upload, login, init, delete, run


def build_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"DeepMux\ncommand-line interface",
        epilog="deepmux-cli, https://deepmux.com"
    )

    subparsers = parser.add_subparsers(help="options", dest="mode")

    subparsers.add_parser("login", help="authorize cli to access deepmux the API")

    subparsers.add_parser("init", help="initialize a project in current directory")

    subparsers.add_parser("upload", help="upload the project in current directory")

    subparsers.add_parser("env", help="list available environments")

    subparsers.add_parser("list", help="list created functions")

    delete_parser = subparsers.add_parser("delete", help="delete function")
    delete_parser.add_argument("--name", help="function name", type=str, required=True)

    run_parser = subparsers.add_parser("run", help="run function")
    run_parser.add_argument("--name", help="function name", type=str, required=True)
    run_parser.add_argument("--file", help="data file", type=str)
    run_parser.add_argument("--data", help="data", type=str)

    return parser


def main():
    parser = build_parser()
    config.args = parser.parse_args()

    if config.args.mode == 'login':
        login()
    elif config.args.mode == 'init':
        init()
    elif config.args.mode == 'upload':
        upload()
    elif config.args.mode == 'env':
        env()
    elif config.args.mode == 'list':
        list_()
    elif config.args.mode == 'delete':
        delete(name=config.args.name)
    elif config.args.mode == 'run':
        run(name=config.args.name, file=config.args.file, data=config.args.data)
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
