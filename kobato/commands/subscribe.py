from kobato.plugin import KobatoBasePlugin, kobato_plugin_register

class KobatoSubscribe(KobatoBasePlugin):
    pass
    
kobato_plugin_register('subscribe', KobatoSubscribe, aliases = ('s', 'sub'), description = "Manage your subscriptions to posts, users and tags")
