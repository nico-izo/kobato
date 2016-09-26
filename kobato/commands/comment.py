import sys

from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import Api, auth_required
from kobato.prompt import confirm


class KobatoComment(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-m', '--message', action='append', help='Text of the comment', default=[])
        parser.add_argument('-p', '--post', action='append', default=[], help='Post comment to #post (or just post) or answer to #comment/id (or just comment/id)')
        # TODO: edit
        # TODO: yes
        # TODO: editor, force editor, supress editor, multiple at same time

    @auth_required
    def run(self, args):
        if len(args['message']) != len(args['post']):
            print('You must have equal amount entities to respond and provided messages')
            sys.exit(1)

        for i in zip(args['post'], args['message']):
            self._comment(*i)
            print('')

    # TODO: --yes, jinja, settings
    def _comment(self, to, message):
        message = message.strip()

        if len(message) == 0:
            print('Comment cannot be empty')
            sys.exit(1)

        to = to.split('/')
        to[0] = to[0][1:] if to[0].startswith('#') else to[0]

        print('Comment to #{}:'.format('/'.join(to)))
        print('='*10)
        print(message)
        print('='*10)

        y = confirm(text='Confirm?')

        if y != ['y']:
            print('Skipping...')
            return

        res = None

        if len(to) == 1:
            res = self._api.create_comment(to[0], message)
        elif len(to) == 2:
            res = self._api.create_comment(to[0], message, to[1])
        else:
            print('Invalid post/comment ID. Exiting.')
            sys.exit(1)

        print('Comment #{}/{} has been posted'.format(res['id'], res['comment_id']))


kobato_plugin_register('comment', KobatoComment, aliases=['c'], description="Write comments and edit them")
