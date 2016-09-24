import sys

from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import Api, auth_required


class KobatoSubscribe(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-U', '--unsub', action='store_true', default=False, help='Use this key to unsubscribe')
        parser.add_argument('object', nargs='*', help='#thread or @user')
        parser.add_argument('-u', '--user', action='append', help='Specify user or @user', default=[])
        parser.add_argument('-p', '--post', action='append', help='Specify thread or #thread', default=[])
        parser.add_argument(
            '-r',
            '--recs',
            action='store_true',
            help='Sub (or unsub) ONLY to recommendations of the user. '
                 'Used like -U flag, so you cannot combine it with regular subscribe or unsubscribe'
        )

    def _check_and_dispatch(self, objs, args):
        """
        Checks that every string in objs starts with # or @
        and moves them to args['post'] and args['user'] accordingly
        """
        valid = True
        for i in objs:
            if not i.startswith('#') and not i.startswith('@'):
                valid = False
                break
            elif i.startswith('#'):
                args['post'].append(i)
            else:
                args['user'].append(i)

        return valid

    @auth_required
    def run(self, args):
        if args['object']:
            if not self._check_and_dispatch(args['object'], args):
                print('If you are using generalized parameter, you must prefix threads with # and users with @')
                sys.exit(1)

        # First boolean — subscribe/unsub
        # Second — not recs/recs
        do_with_user = {
            # UNSUB IS_REC
            (False, False): self._api.sub_to_user,
            (True,  False): self._api.unsub_from_user,
            (False,  True): self._api.sub_to_user_recs,
            (True,   True): self._api.unsub_from_user_recs
        }[(args['unsub'], args['recs'])]

        do_with_thread = self._api.sub_to_post if not args['unsub'] else self._api.unsub_from_post

        for user in args['user']:
            user_ = user[1:] if user.startswith('@') else user
            print("{} @{}'s {}".format(
                'Subscribing to' if not args['unsub'] else 'Unsubscribing from',
                user_,
                'posts and recommendations' if not args['recs'] else 'recommendations ONLY'
            ))
            result = do_with_user(user_)
            print("Subscribed" if not args['unsub'] else "Unsubscribed")

        for thread in args['post']:
            thread_ = thread[1:] if thread.startswith('#') else thread
            print('{} #{}...'.format(
                'Subscribing to' if not args['unsub'] else 'Unsubscribing from',
                thread_
            ))
            result = do_with_thread(thread_)
            print("Subscribed" if not args['unsub'] else "Unsubscribed")

kobato_plugin_register('subscribe', KobatoSubscribe, aliases=['s', 'sub'], description="Manage your subscriptions to posts, users and tags")
