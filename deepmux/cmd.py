import os
import sys
import yaml
import uuid
import shutil
import typing
import getpass

from yaml.parser import ParserError

from deepmux.config import config
from deepmux.api import API
from deepmux.templates import python_function_basic
from deepmux.errors import UnknownException, NotFound


def login(skip_if_logged: bool = False):
    if skip_if_logged and os.path.exists(config.deepmux_token_path):
        return

    os.system(f"mkdir -p {config.deepmux_dir_path}")
    print("Get your token from https://app.deepmux.com/api_key")
    token = input('token: ')
    with open(config.deepmux_token_path, 'w') as token_file:
        token_file.write(token)
    print('done')


def init():
    with open('deepmux.yaml', 'w') as deepmux_yaml:
        deepmux_yaml.write(python_function_basic)
    with open('.deepmuxignore', 'w') as deepmux_ignore:
        deepmux_ignore.write('.deepmuxignore\n')

    print("./deepmux.yaml created.")
    print("Fill it to get started.")


def _load_ignore() -> typing.List[str]:
    try:
        with open('.deepmuxignore', 'r') as deepmux_ignore:
            return deepmux_ignore.readlines()
    except FileNotFoundError:
        return []


def _parse_function_name() -> str:
    with open('deepmux.yaml') as file:
        deepmux_yaml = yaml.safe_load(file)
        return deepmux_yaml['name']


def upload():
    try:
        name = _parse_function_name()
    except FileNotFoundError:
        print('deepmux.yaml not found. Please initialize the project with \'deepmux init\'')
        return
    except ParserError:
        print('failed to parse deepmux.yaml')
        return

    try:
        API.get_function(name=name)
    except NotFound:
        print('Creating function...')
        API.create(name=name)
    print('Compressing function data...')
    uid = str(uuid.uuid4())[:6]
    zip_file_name = f".{uid}_deepmux"
    copy_dir_name = f".{uid}_copy"
    ignore = shutil.ignore_patterns(*_load_ignore())
    try:
        shutil.copytree('./', copy_dir_name, ignore=ignore)
        shutil.make_archive(zip_file_name, 'zip', copy_dir_name)
        print('Uploading function data...')
        with open(f"{zip_file_name}.zip", 'rb') as f:
            API.upload(name=name, payload=f)
    finally:
        try:
            os.unlink(f"{zip_file_name}.zip")
        except OSError:
            pass
        shutil.rmtree(copy_dir_name, ignore_errors=True)
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


def delete(*, name: str):
    API.delete(name)
    print(f'function {name} deleted')


def run(*, name: str, data: str = None, file: str = None):
    if file is not None:
        try:
            with open(file, 'r') as file:
                data = file.read()
        except FileNotFoundError:
            print('file not found')
    if data is not None:
        sys.stdout.buffer.write(API.run(name=name, data=data))
    else:
        print("please specify --data or --file argument")


__all__ = ('env', 'list_', 'init', 'upload', 'login', 'delete', 'run')
