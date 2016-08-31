from ..commands.feed import render_post

def test_render_post():
    post_obj = {
        'post': {
            'author':{
                'login': 'test_user'
            },
            'comments_count': 3,
            'created': '2016-08-31T18:54:14.543343',
            'text': 'test message\nnewline',
            'tags': ['foo', 'bar', 'baz baz baz'],
            'type': 'post',
            'private': False,
            'pinned': False,
            'id': 'foobaz'
        },
        'subscribed': True,
        'recommended': False,
        'bookmarked': False,
        'editable': False
    }

    post_txt = """@test_user:
*foo, bar, baz baz baz

test message
newline

#foobaz created at 2016-08-31T18:54:14.543343
Comments: 3"""

    assert render_post(post_obj) == post_txt, "Check basic rendering"
