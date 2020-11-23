import os


class _Config(object):

    def __init__(self):
        self.args = None
        self.token = None
        self.home = os.getenv('HOME')
        self.base_url = os.getenv('DEEPMUX_BASE_URL', 'https://api.deepmux.com/v1')

        self.deepmux_dir_path = os.path.join(self.home, '.deepmux')
        self.deepmux_token_path = os.path.join(self.deepmux_dir_path, 'token')


config = _Config()
