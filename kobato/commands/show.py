from kobato.plugin import KobatoBasePlugin, kobato_plugin_register

class KobatoShow(KobatoBasePlugin):
    pass
    
kobato_plugin_register('show', KobatoShow, description = "Used to fetch posts and comments by IDs, tags, nicknames")
