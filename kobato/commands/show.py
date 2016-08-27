from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.config import Config, config_sync, config_flush, is_logged_in

import argparse
import requests
import sys
from getpass import getpass
from decorating import animated

class KobatoShow(KobatoBasePlugin):
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-w', '--whoami', default=False, action='store_true')
        parser.add_argument('-p', '--post', help = 'Show post by ID')
        parser.add_argument('-u', '--user', help = 'Show user by nickname')
        #parser.add_argument('-t', '--tag', help = 'Show posts by, well, *tag')
        parser.add_argument('-r', '--replies', help = 'Show replies to post', default=False, action='store_true')

        if not len(self._args):
            self._args = ['--help']

        self._parsed_args = vars(parser.parse_args(self._args))

        if self._parsed_args['whoami']:
            if not is_logged_in():
                print("You are NOT logged in. Terminating.")
                return

            print("Login: {0}".format(Config['login']['login']))

            print("Retrieving information from point.im...")
            self.user_info(Config['login']['login'])

            return

        if self._parsed_args['user']:
            print("Retrieving information about {0}".format(self._parsed_args['user']))
            self.user_info(self._parsed_args['user'])
            return

        if self._parsed_args['post']:
            print("Loading", self._parsed_args['post'])

            self.post(self._parsed_args['post'], self._parsed_args['replies'])

            return

    def post(self, post, replies = False):
        post_ = post[1:] if post.startswith('#') else post

        with animated("Preparing to read #{0}".format(post_)):
            r = requests.get(
                "https://point.im/api/post/{0}".format(post_),
                headers = {
                    'Authorization': Config['login']['token']
                    }
                )

        try:
            res = r.json()
            if 'error' in res:
                print("Something went wrong:", res['error'])
                return
        except Exception:
            print("JSON parsing failed")
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

    @animated("Doin' stuff...")
    def user_info(self, user):
        user_ = user[1:] if user.startswith('@') else user

        r = requests.get(
            "https://point.im/api/user/login/{0}".format(user_),
            headers = {
                'Authorization': Config['login']['token']
                }
            )

        try:
            res = r.json()
            if 'error' in res:
                print("Something went wrong:", res['error'])
                return
        except Exception:
            print("JSON parsing failed")
            return
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
