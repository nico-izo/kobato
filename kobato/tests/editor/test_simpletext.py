import unittest
from kobato.editor.simpletext import SimpleText

class TestSimpleText(unittest.TestCase):

    def test_creation(self):
        t = SimpleText('foo bar')

        self.assertEqual(t.text, 'foo bar')

    def test_strip(self):
        t = SimpleText('     \t\nfoo\t\n    ')

        self.assertEqual(t.text, 'foo')

    def test_modify_strip(self):
        t = SimpleText('')

        self.assertEqual(t.text, '')

        t.text = '     \t\nfoo \n \t  '
        self.assertEqual(t.text, 'foo')

    def test_encode(self):
        t = SimpleText('text')

        self.assertEqual(t.encode(), 'text')

    def test_decode_encoded(self):
        t = SimpleText('  \n foo bar \n ')

        t2 = SimpleText.decode(t.encode())

        self.assertEqual(t.text, t2.text)

    def test_decode(self):
        t = SimpleText.decode('   \t\n  foo   ')

        self.assertEqual(t.text, 'foo')

    def test_reload(self):
        t = SimpleText('foo')

        t.reload('\tbar\t')

        self.assertEqual(t.text, 'bar')
