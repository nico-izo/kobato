import unittest

from kobato.editor.blogpost import BlogPost


class TestBlogPost(unittest.TestCase):

    def test_creation(self):
        p = BlogPost(text='sample text', tags=['tag 1', 'tag 2', 'tag', 'tag'])

        self.assertEqual(p.text, 'sample text')
        self.assertEqual(p.tags, ['tag 1', 'tag 2', 'tag', 'tag'])
        self.assertEqual(p.private, False)

    def test_modifying(self):
        p = BlogPost(text='sample text', tags=['tag1', 'tag2'])

        p.text = 'new text'

        self.assertEqual(p.text, 'new text')

        p.tags = ['new tag']

        self.assertEqual(p.tags, ['new tag'])

        p.private = True

        self.assertEqual(p.private, True)

    def test_strip(self):
        p = BlogPost(text="""

                     foo bar baz

                     """, tags=['   tag  ', '\ttag\t'])

        self.assertEqual(p.text, 'foo bar baz')
        self.assertEqual(p.tags, ['tag', 'tag'])

        p.text = """
        \t
        test
        \t

        """

        self.assertEqual(p.text, 'test')

        p.tags = ['   \ttag\t   ']

        self.assertEqual(p.tags, ['tag'])

    def test_encode(self):
        p = BlogPost(text='foobar', tags=['tag1', 'tag 2', 'teh 3rd tag'])

        self.assertEqual(p.encode(), '*tag1, tag 2, teh 3rd tag\n'
                                     '\n'
                                     'foobar')

    def test_decoding_of_encoded(self):
        p = BlogPost(text='foo bar baz', tags=['tag 1', 'tag 2'])  # TODO: add tag with commas (will fail now)

        decoded = BlogPost.decode(p.encode())

        self.assertEqual(p.text, decoded.text)
        self.assertEqual(p.tags, decoded.tags)
        self.assertEqual(p.private, decoded.private)

    def test_decoding_post(self):
        text = "*tag 1, tag 2, tag 3\n\nfoobar"

        p = BlogPost.decode(text)

        self.assertEqual(p.text, 'foobar')
        self.assertEqual(p.tags, ['tag 1', 'tag 2', 'tag 3'])
        self.assertEqual(p.private, False)

    def test_encoding_no_tags(self):
        p = BlogPost(text='foo')

        self.assertEqual(p.tags, [])

        self.assertEqual(p.encode(), 'foo')

    def test_decoding_no_tags(self):
        p = BlogPost.decode('foo')

        self.assertEqual(p.text, 'foo')
        self.assertEqual(p.tags, [])
        self.assertEqual(p.private, False)

    def test_decoding_empty(self):
        p = BlogPost.decode('')

        self.assertEqual(p.text, '')
        self.assertEqual(p.tags, [])
        self.assertEqual(p.private, False)

    def test_decode_only_tags(self):
        p = BlogPost.decode('*tag 1, tag 2, tag 3')

        self.assertEqual(p.tags, ['tag 1', 'tag 2', 'tag 3'])
        self.assertEqual(p.text, '')
        self.assertEqual(p.private, False)

    def test_annul_tags(self):
        p = BlogPost(tags=['tag 1'])

        dummy = []
        p.tags = dummy
        dummy.append('tag 2')

        self.assertEqual(p.tags, [])

    def test_add_tag(self):
        p = BlogPost()

        self.assertEqual(p.tags, [])
        p.add_tag('tag')

        self.assertEqual(p.tags, ['tag'])

        p.add_tag('   \n\t  tag 2 \t\t\n ')

        self.assertEqual(p.tags, ['tag', 'tag 2'])

        p.add_tags(['tag 3', '   \n\ttag 4 \n\t'])

        self.assertEqual(p.tags, ['tag', 'tag 2', 'tag 3', 'tag 4'])
