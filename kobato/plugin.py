from decorating import animated
import sys
import re
import shlex

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

# I will probably deeply regret this piece of code
def kobato_format(str_, *args):
    p = re.compile("({\d+}|{...})")
    i = -1
    tail_found = False
    prev = 0
    res = []
    res.append(str_)
    for m in p.finditer(str_):
        s = res.pop()
        res.append(s[0:m.start() - prev])

        if m.group() == "{...}":
            res.append(m.group())
        else:
            res.append(str(args[int(m.group()[1:-1])]))
            i = max(i, int(m.group()[1:-1]))

        res.append(str_[m.end():])
        prev = m.end()
    res = "".join(res)
    i += 1

    return res.replace("{...}", " ".join(map(str, args[i:])))

def kobato_plugin_dispatch(command, args, config):
    aliases = []
    if 'aliases' in config:
        aliases = config['aliases']

    if command in aliases:
        try:
            result = kobato_format(aliases[command], *args)
        except IndexError:
            print("ERROR: not enough arguments for alias")
            sys.exit(1)

        print("Alias resolved: kobato", result)
        print("Executing...")
        result = shlex.split(result)
        command = result[0]
        args = result[1:]

    for key, value in commands.items():
        if key == command or command in value['aliases']:
            process = value['body'](args, config)
            process.run()
            return

    print("ERROR: command {0} not found. See kobato help for list of available commands".format(command))
    sys.exit(1)

if __name__ == '__main__':
    assert kobato_format("{0}", 1) == "1"
    assert kobato_format("{0} {1}", 1, 2) == "1 2"
    assert kobato_format("{1} {1}", 1, 2) == "2 2"
    assert kobato_format("{1} {0}", 1, 2) == "2 1"
    assert kobato_format("{1}", 1, 2) == "2"
    assert kobato_format("{0} {1}", 1, 2, 3) == "1 2"
    assert kobato_format("{0} {1} {...}", 1, 2, 3, 4, 5, 6) == "1 2 3 4 5 6"
    assert kobato_format("{...} {0} {1}", 1, 2, 3, 4, 5, 6) == "3 4 5 6 1 2"
    assert kobato_format("{...}", 1, 2, 3) == "1 2 3"
    assert kobato_format("{3}{2}{1}", 1, 2, 3, 4) == "432"
    assert kobato_format("text", 1, 2, 3, 4) == "text"
    assert kobato_format("text") == "text"
