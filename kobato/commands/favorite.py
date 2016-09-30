from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import Api, auth_required


class KobatoFavorite(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument(
            '-u',
            '--unfavorite',
            action='store_true',
            default=False,
            help='Use this key to unfavorite.'  # Warning: will not remove local file (or files)'
        )
        parser.add_argument('-s', '--show', action='store_true', default=False, help='Show your last 20 bookmarks')
        parser.add_argument('-i', '--interactive', action='store_true', default=False, help='Interactive --show')
        parser.add_argument('object', nargs='*', help='(Un)Favorite posts or post/id (comments).', default=[])
#        parser.add_argument(
#            '-S',
#            '--sync',
#            action='store_true',
#            default=False,
#            help='Sync your local favorites with web'
#        )
#        parser.add_argument(
#            '-F',
#            '--force-dump',
#            action='store_true',
#            help='Force dump post (useful if you have favorites.allow_dump = False in config, otherwise has no effect)'
#        )
        parser.add_argument(
            '-E',
            '--editor',
            action='store_true'
        )

    @auth_required
    def run(self, args):
        if args['unfavorite'] and not len(args['object']):
            print('You need to specify post(s) to use --unfavorite option')
            sys.exit(1)
#        if args['purge'] and not len(args['object']):
#            print('You need to specify post(s) to use --purge option')
#            sys.exit(1)

        if not any([args[i] for i in ('show', 'interactive', 'object')]):  # sync
            args['interactive'] = True

        if args['interactive']:
            self.interactive_show()
            return

        if args['show']:
            self.show()
            return

        if args['sync']:
            self.sync()
            return

        if args['object']:
            self.favorite(args['object'], args['unfavorite'])
            return

    def interactive_show(self):
        pass

    def favorite(self, objs, unfavorite=False):
        for o in args['object']:
            text = None
            if args['editor']:
                text = misc.runEditor()
            splitted = o.split('/')
            if len(splitted) > 2:
                print('Invalid post id:', o)
                sys.exit(1)

            {
                1: self._api.fav_post,
                2: self._api.fav_comment
            }[len(splitted)](*splitted, text)

    def sync(self):
        pass

    def show(self):
        pass

kobato_plugin_register(
    'favorite',
    KobatoFavorite,
    aliases=['f', 'fav'],
    description="Manage your favorites",
    default_aliases={'ufav': 'fav -U'}
)
