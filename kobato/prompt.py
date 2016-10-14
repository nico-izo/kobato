from collections import OrderedDict


class PromptException(Exception):
    pass


class Prompt:
    def __init__(self, allow_multiple=False, case_sensitive=False, text='Choice required'):
        self._allow_multiple = allow_multiple
        self._case_sensitive = case_sensitive
        self._text = text
        self._default = '?'

        self._actions = OrderedDict({
            '?': {
                'help': 'Prints this help message'
                # conflicts with: literally everything else
            }
        })

    def add_action(self, action, help='No help :(', conflicts=None, default=False):
        if not self._case_sensitive:
            action = action.lower()

        if action in self._actions:
            raise PromptException('Action with same name already exists')

        if default:
            self._default = action

        self._actions.update({action: {'help': help}})

        if conflicts is not None:
            self._actions[action]['conflicts'] = conflicts

    # TODO: move to jinja
    def help(self):
        res = []
        res.append('Available actions:')
        for key, value in self._actions.items():
            res.append("   {0} — {1}".format(key, value['help']))

        return '\n'.join(res)

    def _inline_help(self):
        self._actions.move_to_end('?')
        keys = self._actions.keys()
        if not self._case_sensitive:
            keys = map(lambda k: k.upper() if k == self._default else k, keys)

        return '|'.join(keys)

    def input(self):
        str_ = self._inline_help()

        print("{1} [{0}]: ".format(str_, self._text), end='')
        res = input()
        if not self._case_sensitive:
            res = res.lower()

        print()
        cur_conflicts = set()
        out = set()
        while True:
            if res is None:
                print("{1} [{0}]: ".format(str_, self._text), end='')
                cur_conflicts = set()
                out = set()
                res = input()
                print()

            if '?' in res or (res == '' and self._default == '?'):
                print(self.help())
                res = None
                continue

            if res == '':
                out.add(self._default)
                break

            for c in res:
                if c not in self._actions:
                    print("Invalid action:", c)
                    res = None
                    break

                if c in cur_conflicts:
                    print("Action '{0}' conflicts with one of previous actions".format(c))
                    res = None
                    break
                out.add(c)
                if 'conflicts' in self._actions[c]:
                    cur_conflicts.update(self._actions[c]['conflicts'])
            else:
                break

        return list(out)


def confirm(default='yes', text='Can you confirm?', additional=None):
    """
    Creates basic Prompt object with default actions and issues input
    Use cases: when you need to ask confirmation
    """

    p = Prompt(text=text)
    p.add_action('y', help='Yes', conflicts=['n'], default=(default == 'yes'))
    p.add_action('n', help='No', conflicts=['y'], default=(default == 'no'))

    if additional is not None:
        for action in additional:
            p.add_action(action, help=additional[action], default=(default == action))

    return p.input()
