import os
import sys
import uuid
import shutil
import getpass
import argparse

from deepmux.config import config
from deepmux.api import API
from deepmux.templates import python_function_basic
from deepmux.errors import UnknownException


def build_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f"\033[92mDeepMux\ncommand-line interface\x1b[0m",
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

    return parser


def login():
    os.system(f"mkdir -p {config.deepmux_dir_path}")
    print("Get your token from https://app.deepmux.com/api_key")
    token = getpass.getpass('token: ', )
    with open(config.deepmux_token_path, 'w') as token_file:
        token_file.write(token)
    print('done')


def init(*, name: str, env_: str):
    API.init(name=name)
    with open('deepmux.yaml', 'w') as deepmux_yaml:
        deepmux_yaml.write(python_function_basic(name=name, env=env_))
    print("./deepmux.yaml created.")
    print("Fill it to get started.")


def upload(*, name: str):
    uid = str(uuid.uuid4())[:6]
    zip_file_name = f".{uid}_deepmux"
    shutil.make_archive(zip_file_name, 'zip', os.getcwd())
    with open(f"{zip_file_name}.zip", 'rb') as project_zip_file:
        try:
            payload = project_zip_file.read()
        finally:
            os.unlink(f"{zip_file_name}.zip")
    API.upload(name=name, payload=payload)
    print('done')


def env():
    function_envs = API.function_envs()
    try:
        envs = function_envs["envs"]
        for item in envs:
            print("name:", item["name"], "language:", item["language"])
    except Exception as e:
        raise UnknownException(repr(e))


def list_():
    functions = API.list_()
    try:
        envs = functions["functions"]
        for item in envs:
            print("name:", item["name"], "state:", item["state"])
    except Exception as e:
        raise UnknownException(repr(e))


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
    else:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
