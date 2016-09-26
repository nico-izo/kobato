from appdirs import user_config_dir

import warnings
import yaml
import os

class ConfigPrivate:
    _config = {}
    _config_name = 'kobato.yaml'

    def __init__(self, path=None):
        self._config_dir = user_config_dir("kobato")

        if os.environ.get('KOBATO_CONFIG') is not None:
            self._config_dir = os.environ.get('KOBATO_CONFIG')

        if path is not None:
            self._config_dir = path

        self._config_path = os.path.join(self._config_dir, self._config_name)

        if not os.path.exists(self._config_path):
            self._create_config()
            print("Config not found, created one in {}".format(self._config_path))
        elif os.path.exists(self._config_path) and not os.path.isfile(self._config_path):
            warning("kobato.yaml exists and NOT file. Exiting", Warning)
            sys.exit(1)
        elif os.path.exists(self._config_path) and os.path.isfile(self._config_path):
            self._load_config()

    def get(self, key, default=None):
        return self._config.get(key, default)

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value

    def __delitem__(self, key):
        del self._config[key]

    def __contains__(self, key):
        return key in self._config

    def _load_config(self):
        with open(self._config_path, 'r') as cfg:
            self._config = yaml.load(cfg.read())
            # if you somehow ended with empty config...
            if self._config is None:
                self.flush()
                self.dump()

    def dump(self):
        with open(self._config_path, 'w') as cfg:
            yaml.dump(self._config, cfg)

    def flush(self):
        if self._config is None:
            self._config = {}

        self._config['login'] = {
            'login': '',
            'password': '',
            'is_logged_in': False
        }

    def _create_config(self):
        self.flush()
        os.makedirs(self._config_dir, exist_ok=True)
        self.dump()

    def is_logged_in(self):
        return self._config.get('login', {}).get('is_logged_in', False)
