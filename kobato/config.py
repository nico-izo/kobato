from os import path
from os import makedirs
from configparser import ConfigParser
from appdirs import user_config_dir

KOBATO_CONFIG = 'kobato.ini'
CONFIG_DIR = user_config_dir("kobato")
CONFIG_PATH = path.join(CONFIG_DIR, KOBATO_CONFIG)

def config_load():
    config = ConfigParser()
    config.read(CONFIG_PATH)
    
    if 'login' not in config:
        config = config_create()

    return config

def config_create():
    config = ConfigParser()
    
    config['login'] = {
        'login': '', 
        'password': '',
        'is_logged_in': 0
    }
    
    makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, 'w') as cfg:
        config.write(cfg)
        print("Config not found, created one in {}".format(CONFIG_PATH))

    return config

Config = config_load()

# what the hell?
def config_sync():
    global Config
    with open(CONFIG_PATH, 'w') as cfg:
        Config.write(cfg)
        
def config_flush():
    global Config
    Config['login'] = {
        'login': '', 
        'password': '',
        'is_logged_in': 0
    }

def is_logged_in():
    global Config
    return 'is_logged_in' in Config['login'] and Config['login']['is_logged_in']
    

# TODO: remove global config, replace with single one
class ConfigPrivate:
    def __init__(self):
        pass
    def __getitem__(self, key):
        pass
    def __setitem__(self, key, value):
        pass
    def __delitem__(self, key):
        pass
    def __contains__(self, key):
        pass
