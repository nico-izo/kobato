from kobato.api import Api

import sys
import re


class KobatoBasePlugin:
    def __init__(self, config):
        self._config = config
        self._api = Api(config)

    def prepare(self, parser):
        """
        Register all of the --keys in this method
        """
        raise NotImplementedError

    def run(self, args):
        raise NotImplementedError

commands = {}

def kobato_plugin_register(
    command,
    _class,
    aliases=None,
    description="No description",
    default_aliases=None):
    global commands

    if aliases is None:
        aliases = []

    commands[command] = {
        'aliases': aliases,
        'body': _class,
        'description': description,
        'default_aliases': default_aliases
    }


# I will probably deeply regret this piece of code
def kobato_format(str_, *args, separator=' '):
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

    return res.replace("{...}", separator.join(map(str, args[i:])))


def kobato_subparsers_register(parser, config, aliases):
    global commands
    for key, value in commands.items():
        subparser = parser.add_parser(key, help=value['description'], aliases=value['aliases'])
        plugin = value['body'](config)
        plugin.prepare(subparser)

        subparser.set_defaults(func=plugin.run)

        if value['default_aliases'] is not None:
            aliases.update(value['default_aliases'])
