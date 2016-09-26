import sys

from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import Api, auth_required
from kobato.prompt import confirm


class KobatoDelete(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-y', '--yes', action='store_true', help='DANGEROUS: Do not ask for confirmation')
        parser.add_argument('object', nargs='*', help='Delete thread, #thread, comment/id or #comment/id')

        # TODO: backup before deletion
    @auth_required
    def run(self, args):
        print('You are about to permanently remove some of your posts or comments')

        if not(args['object']):
            print('No entities specified. Exiting')
            sys.exit(1)

        def _wtf(entity):
            def func(_):
                print('Invalid post or comment id: #{}'.format(entity))

            return func

        for i in args['object']:
            entity_ = i[1:] if i.startswith('#') else i

            if not args['yes']:
                    r = confirm(default='no', text='Deleting #{}. Confirm?'.format(entity_))
                    if r == ['n']:
                        print('Leaving it untouched')
                        continue

            res = {
                1: lambda a: a.delete_post(entity_),
                2: lambda a: a.delete_comment(*entity_.split('/'))
            }.get(
                len(entity_.split('/')),
                _wtf(entity_)
            )(self._api)

            print("Post #{0} has been removed successfully".format(entity_))


kobato_plugin_register('delete', KobatoDelete, aliases=['d', 'del'], description="Delete your posts or comments")
