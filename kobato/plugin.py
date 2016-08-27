from decorating import animated

class KobatoBasePlugin:
    def __init__(self, args):
        self._args = args
        
    def run(self):
        print("Somebody! Please implement me!")

class KobatoDummy(KobatoBasePlugin):
    def run(self):
        print(self._args)

commands = {
    'dummy': {
        'aliaces': ('lebabufalo'),
        'body': KobatoDummy,
        'description': 'I\'m a dummy. Don\'t mind me.'
    }
}

def kobato_plugin_register(command, _class, aliases = (), description = "TODO"):
    commands[command] = {
        'aliases': aliases,
        'body': _class,
        'description': description
    }

def kobato_plugin_dispatch(command, args):
    for key, value in commands.items():
            process = value['body'](args)
        if key == command or command in value['aliases']:
            process.run()
            return

    print("ERROR: command {0} not found. See kobato help for list of available commands".format(command))
    sys.exit(1)

