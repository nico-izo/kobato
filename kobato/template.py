from jinja2 import Template, Environment, PackageLoader
env = Environment(
    loader=PackageLoader('kobato', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)

templates = {}

templates['post'] = """"""


def template(name):
    #if name not in templates:
    #    raise Exception

    #return Template(templates[name])

    template = env.get_template('{0}.jinja'.format(name))
    return template
