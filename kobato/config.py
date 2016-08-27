from os import path
from os import makedirs
#from configparser import ConfigParser
import yaml
from appdirs import user_config_dir

import warnings

#KOBATO_CONFIG = 'kobato.yaml'
#CONFIG_DIR = user_config_dir("kobato")
#CONFIG_PATH = path.join(CONFIG_DIR, KOBATO_CONFIG)

#def config_load():
    #config = ConfigParser()
    #config.read(CONFIG_PATH)

    #if 'login' not in config:
        #config = config_create()

    #return config

#def config_create():
    #config = ConfigParser()

    #config['login'] = {
        #'login': '',
        #'password': '',
        #'is_logged_in': 0
    #}

    #makedirs(CONFIG_DIR, exist_ok=True)
    #with open(CONFIG_PATH, 'w') as cfg:
        #config.write(cfg)
        #print("Config not found, created one in {}".format(CONFIG_PATH))

    #return config

##Config = config_load()

## what the hell?
#def config_sync():
    #global Config
    #with open(CONFIG_PATH, 'w') as cfg:
        #Config.write(cfg)

#def config_flush():
    #global Config
    #Config['login'] = {
        #'login': '',
        #'password': '',
        #'is_logged_in': 0
    #}


# TODO: remove global config, replace with single one
class ConfigPrivate:
    _config = {}
    _config_name = 'kobato.yaml'

    def __init__(self):
        self._config_dir = user_config_dir("kobato")
        self._config_path = path.join(self._config_dir, self._config_name)

        if not path.exists(self._config_path):
            self._create_config()
            print("Config not found, created one in {}".format(self._config_path))
        elif path.exists(self._config_path) and not path.isfile(self._config_path):
            warning("kobato.yaml exists and NOT file. Exiting", Warning)
            sys.exit(1)
        elif path.exists(self._config_path) and path.isfile(self._config_path):
            self._load_config()

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
            # if you somehow ended as empty config...
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
            'is_logged_in': 0
        }

    def _create_config(self):
        self.flush()
        makedirs(self._config_dir, exist_ok=True)
        self.dump()

    def is_logged_in(self):
        return 'is_logged_in' in self._config['login'] and self._config['login']['is_logged_in']

config = ConfigPrivate()
