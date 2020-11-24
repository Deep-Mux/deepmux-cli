import os
import uuid
import shutil
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


def delete(*, name: str):
    API.delete(name)
    print(f'function {name} deleted')


__all__ = ('env', 'list_', 'init', 'upload', 'login', 'delete')
