from kobato.plugin import KobatoBasePlugin, kobato_plugin_register


class KobatoSubscribe(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-u', '--unsub', action='store_true', default=False, help='Use this key to unsubscribe')
        parser.add_argument('object', nargs='*', help='Subscribe to #thread, @user or *tag')

    def run(self, args):
        pass


kobato_plugin_register('subscribe', KobatoSubscribe, aliases=['s', 'sub'], description="Manage your subscriptions to posts, users and tags")
