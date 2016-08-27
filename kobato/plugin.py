from decorating import animated

class KobatoBasePlugin:
    def __init__(self, args, config):
        self._args = args
        self._config = config

    def run(self):
        print("Somebody! Please implement me!")

class KobatoDummy(KobatoBasePlugin):
    def run(self):
        print(self._args)

commands = {}

def kobato_plugin_register(command, _class, aliases = (), description = "TODO"):
    commands[command] = {
        'aliases': aliases,
        'body': _class,
        'description': description
    }

def kobato_plugin_dispatch(command, args, config):
    aliases = []
    if 'aliases' in config:
        aliases = config['aliases']

    for key, value in commands.items():
        if key == command or command in value['aliases']:
            process = value['body'](args, config)
            process.run()
            return

    print("ERROR: command {0} not found. See kobato help for list of available commands".format(command))
    sys.exit(1)

