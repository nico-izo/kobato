from kobato.plugin import KobatoBasePlugin, kobato_plugin_register

import argparse
import sys

class KobatoAlias(KobatoBasePlugin):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-l', '--list', default=False, action='store_true')
        parser.add_argument('-c', '--create', nargs=2, help = 'Create new alias', metavar = ('alias_name', 'alias_body'))
        parser.add_argument('-d', '--delete', help = 'Delete alias by name')
        parser.add_argument('-f', '--force', help = 'Force action', default=False, action='store_true')

        if not len(self._args):
            self._args = ['--help']

        self._parsed_args = vars(parser.parse_args(self._args))

        if self._parsed_args['list']:

            print("List of user-defined aliases. For built-in aliases, run kobato help\n")

            print("Current aliases:\n")

            if 'aliases' not in self._config or not len(self._config['aliases']):
                print("Nothing found")
                return

            for key, value in self._config['aliases'].items():
                print("   {0} => {1}".format(key, value))

            return

        if self._parsed_args['create']:
            if 'aliases' not in self._config:
                self._config['aliases'] = {}

            alias_name = self._parsed_args['create'][0]
            alias_body = self._parsed_args['create'][1]
            if alias_name in self._config['aliases'] and not self._parsed_args['force']:
                print("ERROR: alias with same name already exists. Use --force to replace or --list to view list of aliases")
                sys.exit(1)

            self._config['aliases'][alias_name] = alias_body
            self._config.dump()
            print("Alias {0} added".format(alias_name))
            return

        if self._parsed_args['delete']:
            alias_name = self._parsed_args['delete']

            if 'aliases' not in self._config or alias_name not in self._config['aliases']:
                print("Alias {0} not found".format(self._parsed_args['delete']))
                return

            del self._config['aliases'][alias_name]
            self._config.dump()
            print("Alias {0} deleted".format(alias_name))






kobato_plugin_register('alias', KobatoAlias, description = "Manage your aliases")
