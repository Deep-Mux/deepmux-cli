import json
import typing
import requests
from urllib.parse import urljoin

from deepmux.config import config
from deepmux.errors import UnknownException, NotFound, NameConflict, LoginRequired


class API(object):

    @staticmethod
    def _get_token() -> str:
        try:
            with open(config.deepmux_token_path, 'r') as file:
                data = file.read()
            if not data:
                raise Exception
        except Exception:
            raise LoginRequired("Please log in first. Use \"deepmux login\"")
        return data

    @classmethod
    def create(cls, *, name: str):
        cls._do_request(suffix=f'function/{name}', method='PUT')

    @classmethod
    def get_function(cls, *, name: str):
        cls._do_request(suffix=f'function/{name}', method='GET')

    @classmethod
    def upload(cls, *, name: str, payload: typing.IO):
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
        return cls._do_request(suffix=f"function/{name}/run", method='POST', data=data, binary=True)

    @staticmethod
    def _raise_for_status(response, method, url):
        detail = f'Request: {method} {url}'
        status_code = response.status_code
        if status_code == 404:
            raise NotFound(detail)
        elif status_code == 409:
            raise NameConflict(detail)
        elif status_code == 200:
            ...
        else:
            raise UnknownException(f'HTTP response code: {response.status_code}\n'
                                   f'Response message: {response.text}\n'
                                   f'{detail}')

    @classmethod
    def _do_request(cls, *, suffix: str, method: str, headers: dict = None,
                    data: str = None, params: dict = None, files: dict = None, binary: bool = False) -> typing.Union[dict, str]:
        headers = dict() if headers is None else {**headers}
        try:
            headers['x-token'] = cls._get_token()
            endpoint = urljoin(config.base_url, suffix)
            response = requests.request(method, endpoint, headers=headers,
                                        data=data, params=params, files=files)
            cls._raise_for_status(response, method, endpoint)
            if binary:
                return response.content
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return response.text
        except NotFound as e:
            raise e
        except NameConflict as e:
            raise e
        except LoginRequired as e:
            raise e
        except Exception as e:
            raise UnknownException(repr(e))
