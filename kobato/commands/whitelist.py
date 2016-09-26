from kobato.plugin import KobatoBasePlugin, kobato_plugin_register


class KobatoWhitelist(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-s', '--show', action='store_true', help='Show your current whitelist')
        parser.add_argument('-U', '--unwhitelist', action='store_true', help='Flag to unwl someone')
        parser.add_argument('object', nargs='*', help='Persons (or @persons) to (un)whitelist')

    def run(self, args):
        pass


kobato_plugin_register('whitelist', KobatoWhitelist, aliases=['wl'], description="Manage your whitelist")
