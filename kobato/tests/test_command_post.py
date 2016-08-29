from ..commands.post import parse_post

def test_parse_post():

    post1 = """*tag1, tag 2, тэг 3 ____
body"""

    post1_res = {
        'private': False,
        'text': 'body',
        'tags': ['tag1', 'tag 2', 'тэг 3 ____']
    }

    assert parse_post(post1, False) == post1_res, "Basic test"

    post1_res['private'] = True

    assert parse_post(post1, True) == post1_res, "Check private flag"

    post1 = """*tag1,tag 2,тэг 3 ____
body"""

    assert parse_post(post1, True) == post1_res, "Remove spaces in tags"

    post1 = """*tag1,tag 2,тэг 3 ____





body





    """

    assert parse_post(post1, True) == post1_res, "Check stripping of post"


    post1 = """*    tag1  \t   ,       \t    tag 2   ,    \t  тэг 3 ____
body
    """

    assert parse_post(post1, True) == post1_res, "Check stripping of tags"

    post1 = """*tag1, tag 2, тэг 3 ____
body
    second line
    third line
    """

    post1_res['text'] = """body
    second line
    third line"""

    assert parse_post(post1, True) == post1_res, "Indentation in post body should remain safe"
