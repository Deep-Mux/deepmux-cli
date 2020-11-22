import os
import json
import requests

from deepmux.config import config
from deepmux.errors import UnknownException, LoginRequired, NotFound, NameConflict


class API(object):

    @staticmethod
    def _get_token() -> str:
        with open(config.deepmux_token_path, 'r') as file:
            return file.read()

    @classmethod
    def init(cls, *, name: str):
        cls._do_request(suffix=f'function/{name}', method='PUT')

    @classmethod
    def upload(cls, *, name: str, payload: bytes):
        cls._do_request(suffix=f'function/{name}', method='POST', files={'repo': payload})

    @classmethod
    def function_envs(cls) -> dict:
        return cls._do_request(suffix='function_envs', method='GET')

    @classmethod
    def list_(cls) -> dict:
        return cls._do_request(suffix='function', method='GET')

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
                    data: dict = None, params: dict = None, files: dict = None) -> dict:
        headers = dict() if headers is None else {**headers}
        try:
            headers['x-token'] = cls._get_token()
            endpoint = os.path.join(config.base_url, suffix)
            response = requests.request(method, endpoint, headers=headers,
                                        json=data, params=params, files=files)
            cls._raise_for_status(response.status_code, endpoint)
            return json.loads(response.text)
        except FileNotFoundError as e:
            raise LoginRequired(repr(e))
        except Exception as e:
            raise UnknownException(repr(e))
