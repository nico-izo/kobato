from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.misc import kobato_request

import argparse
import sys
from getpass import getpass

class KobatoShow(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-w', '--whoami', default=False, action='store_true')
        parser.add_argument('-p', '--post', help = 'Show post by ID')
        parser.add_argument('-u', '--user', help = 'Show user by nickname')
        #parser.add_argument('-t', '--tag', help = 'Show posts by, well, *tag')
        parser.add_argument('-r', '--replies', help = 'Show replies to post', default=False, action='store_true')

    def run(self, args):
        if args['whoami']:
            if not self._config.is_logged_in():
                print("You are NOT logged in. Terminating.")
                return

            print("Login: {0}".format(self._config['login']['login']))

            print("Retrieving information from point.im...")
            self.user_info(self._config['login']['login'])

            return

        if args['user']:
            print("Retrieving information about {0}".format(args['user']))
            self.user_info(args['user'])
            return

        if args['post']:
            print("Loading", args['post'])

            self.post(args['post'], args['replies'])

            return

    def post(self, post, replies = False):
        post_ = post[1:] if post.startswith('#') else post

        res = kobato_request("https://point.im/api/post/{0}".format(post_),
                             method = 'get',
                             ssl_check = True,
                             animated_text = "Preparing to read #{0}".format(post_),
                             headers = {
                                # TODO: do something about actions with optional auth
                                'Authorization': self._config['login']['token']
                             })

        if 'error' in res:
            print("Something went wrong:", res['error'])
            return

        print("")
        print("@{0}: ".format(res['post']['author']['login']))
        print("*" + ", ".join(res['post']['tags']) + "\n")
        print(res['post']['text'])
        print("#{0}".format(res['post']['id']) + " created at " + res['post']['created'])

        print("Comments:", res['post']['comments_count'])

        if replies and res['post']['comments_count']:
            self.render_comments(res['comments'])

    def render_comments(self, comments):
        for c in comments:
            print("@{0}: ".format(c['author']['login']))
            print(c['text'])
            print("{2}#{0}/{1}".format(c['post_id'], c['id'], "! " if c['is_rec'] else ""), end='' if c['to_comment_id'] is not None else "\n")
            if c['to_comment_id'] is not None:
                print(" replied to #{0}/{1}".format(c['post_id'], c['to_comment_id']))
            print("")

    def user_info(self, user):
        user_ = user[1:] if user.startswith('@') else user

        res = kobato_request("https://point.im/api/user/login/{0}".format(user_),
                             method = 'get',
                             ssl_check = True,
                             headers = {
                                # TODO: do something about actions with optional auth
                                'Authorization': self._config['login']['token']
                             })


        if 'error' in res:
            print("Something went wrong:", res['error'])
            sys.exit(1)

        f = lambda x : x in res and res[x] is not None and res[x] != ''

        print("")
        print("@{0}".format(user_) + ":")

        if f('about'):
            print("About:", res['about'])
        if f('xmpp'):
            print("XMPP:", res['xmpp'])
        if f('name'):
            print("Name:", res['name'])

        print("Gender:", self.gender_to_str(res['gender']))

        if f('birthdate'):
            print("Birthdate:", res['birthdate'])

        if f('skype'):
            print("Skype:", res['skype'])
        if f('icq'):
            print("ICQ:", res['icq'])
        if f('homepage'):
            print("Homepage:", res['homepage'])
        if f('email'):
            print("E-mail:", res['email'])
        if f('location'):
            print("Location:", res['location'])

        print("")
        if f('subscribed'):
            print("You are {0}subscribed to this user".format("" if res['subscribed'] else "NOT "))
        if f('rec sub'):
            print("You are {0}subscribed to recommendations".format("" if res['rec sub'] else "NOT "))
        if f('wl'):
            print("This user is {0}in your WL".format("" if res['wl'] else "NOT "))

        # TODO format
        print("Created:", res['created'])
        if res['deny_anonymous']:
            print("This blog is for registered users only")
        if res['private']:
            print("This blog is protected by whitelist")


    def gender_to_str(self, gender):
        if gender is None:
            return "Ugnich"
        elif gender:
            return "Male"
        else:
            return "Female"


kobato_plugin_register('show', KobatoShow, description = "Get information about users, their last posts, about posts, comments and tags")
