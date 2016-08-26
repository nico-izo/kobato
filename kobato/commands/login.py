import argparse

from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.config import Config, config_sync, config_flush, is_logged_in

from getpass import getpass
from decorating import animated
from time import sleep
import requests
import sys

class KobatoLogin(KobatoBasePlugin):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--login', help = 'Optional parameter if you want to only type password')
        parser.add_argument('-r', '--reset', action = 'store_true', default = False, help = 'Exit from Point.im and remove creditentials from config')
        self._parsed_args = vars(parser.parse_args(self._args))
        
        if not self._parsed_args['reset']:
            if is_logged_in():
                # TODO: whoami
                print("You are already logged it. Use kobato user --whoami to remind yourself who you are")
                return

            if not self._parsed_args['login']:
                self.login(input('Username: '), getpass())
            else:
                self.login(self._parsed_args['login'], getpass())
        else:
            self.reset()
        
    @animated('Doin\' stuff...')
    def login(self, login, password):
        r = requests.post('http://point.im/api/login', data = {'login': login, 'password': password})
        
        try:
            result = r.json()
        except Exception as e:
            print("JSON decoding failed: {0} \n".format(type(e).__name__))
            print("Exiting...\n")
            return
        
        if 'error' in result: 
            print("Authorization failed. Config not updated \n")
            return

        elif 'token' in result and 'csrf_token' in result:
            Config['login']['token'] = result['token']
            Config['login']['csrf_token'] = result['csrf_token']
            Config['login']['login'] = login
            Config['login']['password'] = password
            Config['login']['is_logged_in'] = '1'
            config_sync()
            print("Successful authorization. Config file updated")
            print("Welcome, @{0}!".format(login))
    
    @animated('Bye-bye...')
    def reset(self):
        if 'csrf_token' not in Config['login']:
            print("CSRF token not found, flushing config...")
            config_flush()
            config_sync()
            return
        
        r = requests.post('https://point.im/api/logout', data = {'csrf_token': Config['login']['csrf_token']})
        # holy fuck! html 403 page in REST API!
        # print(r.text, "\n")
        
        Config['login'] = {}
        config_sync()
        print("See ya!")

        
        
    
kobato_plugin_register('login', KobatoLogin, aliases = ('lo', 'l'), description = "Login. Just type your password and use the damn thing.")
