from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import auth_required


class KobatoWhitelist(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-s', '--show', action='store_true', help='Show your current whitelist')
        parser.add_argument(
            '-U',
            '--unwhitelist',
            action='store_true',
            help='Flag to unwl (global, so you cannot uwl and wl people in one command)'
        )
        parser.add_argument('object', nargs='*', help='Persons (or @persons) to (un)whitelist')

    @auth_required
    def run(self, args):
        unwl = args['unwhitelist']
        wl_func = self._api.unwl_user if unwl else self._api.wl_user

        if args['show']:
            print('Showing your current whitelist...')

            print("\n{}'s whitelist:".format(self._api.login()))
            wl = self._api.wl()
            if not len(wl):
                print("EMPTY")
                return

            print(", ".join(wl))

            return

        pre_text = "Removing {} from whitelist..." if unwl else "Adding {} to whitelist..."

        for u in args['object']:
            user_ = u[1:] if u.startswith('@') else u
            print(pre_text.format(user_))
            res = wl_func(user_)
            print("Done")


kobato_plugin_register(
    'whitelist',
    KobatoWhitelist,
    aliases=['wl'],
    description="Manage your whitelist",
    default_aliases={'uwl': 'wl -U {...}'}
)
