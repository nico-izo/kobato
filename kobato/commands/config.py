from kobato.plugin import KobatoBasePlugin, kobato_plugin_register

import sys


class KobatoConfig(KobatoBasePlugin):
    def prepare(self, parser):
        subparsers = parser.add_subparsers(help='sub-command help')

        set_ = subparsers.add_parser('set', help='Set config values')
        set_.add_argument('name')
        set_.add_argument('value')
        set_.set_defaults(func=self.set)

        show = subparsers.add_parser('show', help='Show config values')
        show.add_argument('name')
        show.set_defaults(func=self.show)

        reset = subparsers.add_parser('reset', help='Remove setting from config')
        reset.add_argument('name')
        reset.set_defaults(func=self.reset)

    def run(self, args):
        # TODO FIXME
        raise NotImplementedError('TODO: SHOW HELP')

    def set(self, args):
        try:
            (group, name) = args['name'].split('.')
        except ValueError:
            print('Please provide path in format: <group>.<name>')
            sys.exit(1)

        val = args['value']

        if self._config.get(group) is None:
            self._config[group] = {}

        val = {
            'true': True,
            'false': False,
            'True': True,
            'False': False
        }.get(val, val)

        self._config[group][name] = val

        self._config.dump()

    def show(self, args):
        path = args['name']

        def print_group(name):
            if self._config.get(name) is None:
                print('No such group in config:', name)
                return

            for line in self._config.get(name):
                print('   {}.{} => {}'.format(name, line, self._config.get(name).get(line)))

        def print_line(group, name):
            if self._config.get(group) is None:
                print('No such group in config:', name)
                return

            if self._config.get(group).get(name) is None:
                print('No such entry found in config')
                return

            print('   {}.{} => {}'.format(group, name, self._config.get(group).get(name)))

        def error(*args, **kwargs):
            print('Invalid format')
            sys.exit(1)

        {
            1: print_group,
            2: print_line
        }.get(len(path.split('.')), error)(*path.split('.'))

    def reset(self, args):
        try:
            (group, name) = args['name'].split('.')
        except ValueError:
            print('You can\'t reset config group. Reset individual entries.'
                  ' Please provide path in format: <group>.<name>')
            sys.exit(1)

        try:
            del self._config[group][name]
        except KeyError:
            pass

        self._config.dump()


kobato_plugin_register(
    'config',
    KobatoConfig,
    aliases=['cfg'],
    description='Set, reset and view kobato config'
)
