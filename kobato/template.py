from jinja2 import Template, Environment, PackageLoader
env = Environment(
    loader=PackageLoader('kobato', 'templates'),
    trim_blocks=True,
    lstrip_blocks=True)


def template(name):
    template = env.get_template('{0}.jinja'.format(name))
    return template

def render(name, kwargs):
    t = template(name)

    return t.render(**kwargs)
