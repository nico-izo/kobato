from collections import OrderedDict


class KobatoPromptException(Exception):
    pass


class KobatoPrompt:
    def __init__(self, allow_multiple=False, case_sensitive=False, text='Choice required'):
        self._allow_multiple = allow_multiple
        self._case_sensitive = case_sensitive
        self._text = text

        self._actions = OrderedDict({
            'h': {
                'help': 'Print this help message'
                # conflicts with: literally everything else
            }
        })

    def add_action(self, action, help='No help :(', conflicts=None):
        if action in self._actions:
            raise KobatoPromptException('Action with same name already exists')

        if not self._case_sensitive:
            action = action.lower()

        self._actions[action] = {'help': help}
        if conflicts is not None:
            self._actions[action]['conflicts'] = conflicts

    # TODO: move to jinja
    def help(self):
        res = []
        res.append('Available actions:')
        for key, value in self._actions.items():
            res.append("   {0} — {1}".format(key, value['help']))

        return '\n'.join(res)

    def input(self):
        self._actions.move_to_end('h')
        str_ = '|'.join(self._actions.keys())

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

            if 'h' in res or res == '':
                print(self.help())
                res = None
                continue

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
