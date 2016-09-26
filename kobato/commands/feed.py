from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.template import render
from kobato.prompt import Prompt
from kobato.api import Api, ApiException, auth_required

import os
import sys
import traceback

class KobatoFeed(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-a', '--all', action='store_true', default=False, help='Show /all instead of your own feed')
        parser.add_argument('-i', '--interactive', action='store_true', default=False, help='Interactive feed')

    def run(self, args):
        if not args['interactive']:
            if args['all']:
                self.feed(f=self._api.all)
            else:
                self.feed(f=self._api.feed)
        else:
            if args['all']:
                self.interactive_feed(feed_func=self._api.all)
            else:
                self.interactive_feed()

    @auth_required
    def feed(self, f=None):
        if f is None:
            f = self._api.feed

        res = f()

        ps = res['posts']

        if not len(ps):
            print("Sorry, no feed for you")
            sys.exit(0)

        for p in ps:
            print(render('post', p))
            print("\n")

    @auth_required
    def interactive_feed(self, feed_func=None):
        if feed_func is None:
            feed_func = self._api.feed
        before = None
        res = feed_func()

        if not len(res['posts']):
            print("Empty feed, exiting...")
            sys.exit(0)

        prompt = Prompt(case_sensitive=True, allow_multiple=True, text='Type desired actions (or ? for help):')
        prompt.add_action('r', help='Recommend without comment', conflicts=['R'])
        prompt.add_action('R', help='Recommend with comment', conflicts=['r'])
        prompt.add_action('f', help='Favorite post')
        prompt.add_action('u', help='After all actions unsub from the post', conflicts=['s'])
        prompt.add_action('s', help='Subscribe to post', conflicts=['u'])
        prompt.add_action('c', help='Open editor to leave comment')
        prompt.add_action('n', help='Next post', conflicts=['p'])
        prompt.add_action('p', help='Previous post', conflicts=['n'])
        prompt.add_action('q', help='After all, quit')

        ps = res['posts']
        i = 0
        api = self._api.clone(sysexit=False)
        while True:
            print('='*10)
            print(render('post', ps[i]))
            print('='*10)
            choice = prompt.input()
            pid = ps[i]['post']['id']

            try:
                if 'f' in choice:
                    api.fav_post(pid)

                if 'r' in choice:
                    api.rec_post(pid)
                elif 'R' in choice:
                    r_text = misc.runEditor(ask_user=True)
                    if r_text == "":
                        print("Empty text field")
                        api.rec_post(pid)
                    else:
                        api.rec_post(pid, r_text)

                if 'c' in choice:
                    c_text = misc.runEditor(ask_user=True)
                    if c_text is None:
                        print("Aborted")
                    else:
                        api.create_comment(pid, c_text)

                if 's' in choice:
                    api.sub_to_post(pid)
                elif 'u' in choice:
                    api.unsub_from_post(pid)

                if 'p' in choice:
                    if i == 0:
                        print("Sorry, but you cannot jump in future")
                    else:
                        i -= 1
                elif 'n' in choice:
                    if i == len(ps) - 1:
                        print("Loading feed...")
                        if not res['has_next']:
                            print("No feed found. Sorry.")

                        res = feed_func(before=ps[i]['uid'])
                        ps.extend(res['posts'])

                    i += 1

                if 'q' in choice:
                    print("Bye!")
                    break
            except ApiException:
                print('Something went wrong during one of your actions')
                print('='*10)
                traceback.print_exc()
                print('='*10)
                print('\nYou can continue your actions.')
                continue


kobato_plugin_register('feed', KobatoFeed, aliases=['f'], description="Read your feed. Es ist an important part of microblogging. Don't forget to read your feed.")
