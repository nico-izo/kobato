import unittest

from kobato.template import render
from kobato.editor.blogpost import BlogPost


class TestPrePostPreview(unittest.TestCase):

    def test_basic(self):
        p = BlogPost(text='foo', tags=['tag 1', 'tag 2'])

        expected = """------
*tag 1, tag 2

foo
------"""

        self.assertEqual(render('pre_post_preview', {'post': p}), expected)

    def test_private(self):
        p = BlogPost(text='foo', tags=['tag 1', 'tag 2', 'tag', 'tag'], private=True)

        expected = """---PRIVATE POST---
*tag 1, tag 2, tag, tag

foo
---PRIVATE POST---"""

        self.assertEqual(render('pre_post_preview', {'post': p}), expected)
