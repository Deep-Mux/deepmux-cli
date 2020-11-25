import os
import uuid
import shutil
import typing
import getpass

from deepmux.config import config
from deepmux.api import API
from deepmux.templates import python_function_basic
from deepmux.errors import UnknownException


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
    with open('.deepmuxignore', 'w') as deepmux_ignore:
        deepmux_ignore.write('.deepmuxignore\n')
        deepmux_ignore.write('deepmux.yaml\n')

    print("./deepmux.yaml created.")
    print("Fill it to get started.")
    print("./.deepmuxignore created")
    print("Write there a list of files and directories that shouldn't be uploaded e.g. venv")


def _load_ignore() -> typing.List[str]:
    try:
        with open('.deepmuxignore', 'r') as deepmux_ignore:
            return deepmux_ignore.readlines()
    except FileNotFoundError:
        return []


def upload(*, name: str):
    uid = str(uuid.uuid4())[:6]
    zip_file_name = f".{uid}_deepmux"
    copy_dir_name = f".{uid}_copy"
    ignore = shutil.ignore_patterns(*_load_ignore())
    shutil.copytree('./', copy_dir_name, ignore=ignore)
    shutil.make_archive(zip_file_name, 'zip', copy_dir_name)
    with open(f"{zip_file_name}.zip", 'rb') as project_zip_file:
        try:
            payload = project_zip_file.read()
        finally:
            os.unlink(f"{zip_file_name}.zip")
            shutil.rmtree(copy_dir_name)
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


def delete(*, name: str):
    API.delete(name)
    print(f'function {name} deleted')


__all__ = ('env', 'list_', 'init', 'upload', 'login', 'delete')
