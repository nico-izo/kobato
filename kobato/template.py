from jinja2 import Template

templates = {}

templates['post'] = """{% if rec %}Recommended by @{{rec.author.login}}{% if rec.text %} as #{{post.id}}/{{rec.comment_id}}: {{rec.text}}{% endif %}
{% endif %}@{{post.author.login}}:
{% if post.tags|length > 0 %}*{% for tag in post.tags %}{% if not loop.first %}, {% endif %}{{tag}}{% endfor %}{% endif %}

{{post.text}}

#{{post.id}} created at {{post.created}}
Comments: {{post.comments_count}}"""

def template(name):
    if name not in templates:
        raise Exception

    return Template(templates[name])

