import sys
import argparse

from deepmux.config import config
from deepmux.cmd import env, list_, upload, login, init, delete


def build_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"DeepMux\ncommand-line interface",
        epilog="deepmux-cli, https://deepmux.com"
    )

    subparsers = parser.add_subparsers(help="options", dest="mode")

    subparsers.add_parser("login", help="authorize cli to access deepmux the API")

    init_parser = subparsers.add_parser("init", help="initialize a project in current directory")

    init_parser.add_argument("--name", help="function name", type=str, required=True)
    init_parser.add_argument("--env", help="environment name e.g. python3.7", type=str, required=True)

    upload_parser = subparsers.add_parser("upload", help="upload the project in current directory")
    upload_parser.add_argument("--name", help="function name", type=str, required=True)

    subparsers.add_parser("env", help="list available environments")

    subparsers.add_parser("list", help="list created functions")

    delete_parser = subparsers.add_parser("delete", help="delete function")
    delete_parser.add_argument("--name", help="function name")

    return parser


def main():
    parser = build_parser()
    config.args = parser.parse_args()

    if config.args.mode == 'login':
        login()
    if config.args.mode == 'init':
        init(name=config.args.name, env_=config.args.env)
    if config.args.mode == 'upload':
        upload(name=config.args.name)
    if config.args.mode == 'env':
        env()
    if config.args.mode == 'list':
        list_()
    if config.args.mode == 'delete':
        delete()
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
