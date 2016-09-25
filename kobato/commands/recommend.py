import sys

from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import Api, auth_required


class KobatoRecommend(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-U', '--unrecommend', action='store_true', help='Use this key to unrecommend')
        parser.add_argument(
            '-m',
            '--message',
            action='append',
            help='Add message. Warning: unavailable for multiple actions'
        )
        parser.add_argument(
            '-E',
            '--editor',
            action='store_true',
            help='Force run editor if you have disabled it (recommend.show_editor)'
        )
        parser.add_argument('-f', '--fast', action='store_true', help='Supress editor if you have enabled it')
        parser.add_argument('-y', '--yes', action='store_true', help='Do not ask for confirmation')
        parser.add_argument('object', nargs='*', help='Recommend thread, #thread, #comment/id or comment/id')

        # TODO:
        # add epilogue about choice:
        # either recommend multiple messages without comment,
        # or see editor for each one of them. OR supply len(args['message']) == len(args['object'])
        # that highlights problem that user may forgot what post was about
        # maybe add syntax for comments?

    def run(self, args):
        pass


kobato_plugin_register('recommend', KobatoRecommend, aliases=['r', 'rec'], description="Recommend and unrecommend posts/comments")
