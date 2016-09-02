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

    post2_obj = {
        'editable': False,
        'rec': {
            'author': {
                'login': 'NokitaKaze',
            },
            'text': 'всё',
            'comment_id': 1
        },
        'recommended': False,
        'bookmarked': False,
        'post': {
            'pinned': False,
            'tags': ['tag@tag', 'tag'],
            'comments_count': 5,
            'text': 'test message\nnewline\n\nnewline',
            'created': '2016-09-02T11:41:13.598825',
            'private': False,
            'type': 'post',
            'id': 'oowqat',
            'author': {
                'login': 'LambdaFM',
            }
        },
        'subscribed': False
    }

    post2_txt = """Recommended by @NokitaKaze as #oowqat/1: всё
@LambdaFM:
*tag@tag, tag

test message
newline

newline

#oowqat created at 2016-09-02T11:41:13.598825
Comments: 5"""

    assert render_post(post2_obj) == post2_txt, "Check recommendation with comment"


    post3_obj = {
        'editable': False,
        'rec': {
            'author': {
                'login': 'cycl0ne',
            },
            'text': None,
            'comment_id': None
        },
        'recommended': False,
        'comment_id': 65,
        'bookmarked': False,
        'post': {
            'pinned': False,
            'tags': ['dybr', 'говно', 'жалкий белок'],
            'comments_count': 83,
            'text': 'блядь. я только понял, что это мой тред. какого хуя вы здесь мне тут устроили?',
            'created': '2016-09-02T12:18:48.338050',
            'private': False,
            'type': 'post',
            'id': 'oowqea',
            'author': {
                'login': 'hirthwork',
            }
        },
        'subscribed': False
    }

    post3_txt = """Recommended by @cycl0ne
@hirthwork:

блядь. я только понял, что это мой тред. какого хуя вы здесь мне тут устроили?

#oowqea/65 posted at 2016-09-02T12:18:48.338050
Comments: 83"""

    assert render_post(post3_obj) == post3_txt, "Check recommendation of comment without comment"
