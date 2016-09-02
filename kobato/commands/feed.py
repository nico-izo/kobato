from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.misc import kobato_request
from kobato.template import template

import os
import sys


def render_post(post):
    # print(post, end='\n\n\n\n\n')
    t = template('post')
    return t.render(**post)


class KobatoFeed(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-n', '--page', metavar=('page'), type=int, help='Show Nth page of feed (warning: limited to 10 pages). Optional parameter')
        parser.add_argument('-i', '--interactive', action='store_true', default=False, help='Interactive feed (TODO: not implemented)')

    def run(self, args):
        if not args['page']:
            self.feed()
        else:
            if args['page'] == 0:
                self.feed()
            elif args['page'] > 1 and args['page'] < 11:
                # TODO
                self.feed()

    def feed(self, before=None):
        if not self._config.is_logged_in():
            print("ERROR: You must be logged in")
            sys.exit(1)

        res = kobato_request('https://point.im/api/recent',
                             method='get',
                             ssl_check=True,
                             animated_text='Nom-nom...',
                             headers={
                                'Authorization': self._config['login']['token']
                             })

        if 'error' in res:
            print("Something went wrong:", res['error'])
            sys.exit(1)

        ps = res['posts']

        if not len(ps):
            print("Sorry, no feed for you")
            sys.exit(0)

        for p in ps:
            print(render_post(p))
            print("\n")


kobato_plugin_register('feed', KobatoFeed, aliases=['f'], description="Read your feed. Es ist an important part of microblogging. Don't forget to read your feed.")
