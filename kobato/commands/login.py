from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import auth_required
from getpass import getpass

import sys


class KobatoLogin(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-l', '--login', help='Optional parameter if you want to only type password')
        parser.add_argument('-r', '--reset', action='store_true', default=False, help='Exit from Point.im and remove credentials from config')

    def run(self, args):
        if not args['reset']:
            if self._config.is_logged_in():
                print("You are already logged it. Use kobato show --whoami to remind yourself who you are")
                return

            if not args['login']:
                self.login(input('Username: '), getpass())
            else:
                self.login(args['login'], getpass())
        else:
            self.reset()

    def login(self, login, password):
        result = self._api.login(login, password)

        if any([x not in result for x in ('token', 'csrf_token')]):
            print('Something wrong with server response. Config not updated. Please report this.')
            sys.exit(120)


        # TODO: this is crap as hell
        self._config['login'] = {}
        self._config['login']['token'] = result['token']
        self._config['login']['csrf_token'] = result['csrf_token']
        self._config['login']['login'] = login
        self._config['login']['password'] = password
        self._config['login']['is_logged_in'] = True
        self._config.dump()
        print("Successful authorization. Config file updated")
        print("Welcome, @{0}!".format(login))

    @auth_required
    def reset(self):
        if 'csrf_token' not in self._config['login']:
            print("CSRF token not found, flushing config...")
            self._config.flush()
            self._config.dump()
            return

        res = self._api.logout()

        self._config.flush()
        self._config.dump()
        print("See ya!")


kobato_plugin_register('login', KobatoLogin, aliases=['lo', 'l'], description="Login. Just type your password and use the damn thing.")
