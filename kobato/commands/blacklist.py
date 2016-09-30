from kobato.plugin import KobatoBasePlugin, kobato_plugin_register


class KobatoBlacklist(KobatoBasePlugin):
    def prepare(self, parser):
        parser.add_argument('-U', '--unblacklist', action='store_true', default=False, help='Remove from blacklist')
        parser.add_argument('-s', '--show', action='store_true', default=False, help='Show your current blacklist')
        parser.add_argument('-u', '--user')
        parser.add_argument('-m', '--message', help='Add optional message about reasons why you hate him/her/whatever. That message will be stored locally')

        parser.add_argument('-b', '--blacklisters', action='store_true', default=False, help='Show users who dared to blacklist your majesty')
        # TODO: edit message (-e?), run editor (eh, another -e? -E?)
        # TODO: maybe allow blacklist multiple at once?

    def run(self, args):
        pass


kobato_plugin_register(
    'blacklist',
    KobatoBlacklist,
    aliases=['bl'],
    description="Add and remove users to/from your blacklist, "
                "view your current blacklist, show users that blacklisted you",
    default_aliases={'ubl': 'bl -U'}
)
