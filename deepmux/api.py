import os
import json
import typing
import requests

from deepmux.config import config
from deepmux.errors import UnknownException, NotFound, NameConflict


class API(object):

    @staticmethod
    def _get_token() -> str:
        with open(config.deepmux_token_path, 'r') as file:
            return file.read()

    @classmethod
    def create(cls, *, name: str):
        cls._do_request(suffix=f'function/{name}', method='PUT')

    @classmethod
    def get_function(cls, *, name: str):
        cls._do_request(suffix=f'function/{name}', method='GET')

    @classmethod
    def upload(cls, *, name: str, payload: bytes):
        cls._do_request(suffix=f'function/{name}', method='POST', files={'repo': payload})

    @classmethod
    def function_envs(cls) -> dict:
        return cls._do_request(suffix='function_envs', method='GET')

    @classmethod
    def list_(cls) -> dict:
        return cls._do_request(suffix='function', method='GET')

    @classmethod
    def delete(cls, name: str) -> dict:
        return cls._do_request(suffix=f'function/{name}', method='DELETE')

    @classmethod
    def run(cls, name: str, data: str):
        return cls._do_request(suffix=f"function/{name}/run", method='POST', data=data)

    @staticmethod
    def _raise_for_status(status_code, url):
        detail = f"url {url}"
        if status_code == 404:
            raise NotFound(detail)
        elif status_code == 409:
            raise NameConflict(detail)
        elif status_code == 200:
            ...
        else:
            raise UnknownException(detail)

    @classmethod
    def _do_request(cls, *, suffix: str, method: str, headers: dict = None,
                    data: str = None, params: dict = None, files: dict = None) -> typing.Union[dict, str]:
        headers = dict() if headers is None else {**headers}
        try:
            headers['x-token'] = cls._get_token()
            endpoint = os.path.join(config.base_url, suffix)
            response = requests.request(method, endpoint, headers=headers,
                                        data=data, params=params, files=files)
            cls._raise_for_status(response.status_code, endpoint)
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return response.text
        except FileNotFoundError:
            print('please log in `deepmux login`')
        except NotFound as e:
            raise e
        except NameConflict as e:
            raise e
        except Exception as e:
            raise UnknownException(repr(e))
