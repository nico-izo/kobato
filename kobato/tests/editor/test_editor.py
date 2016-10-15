import unittest
import subprocess
import tempfile
from unittest import mock

from kobato.editor.texteditor import TextEditor, TextEditorException
from kobato.editor.simpletext import SimpleText


class TestTextEditor(unittest.TestCase):

    def test_subprocess_exists(self):
        # yeah, I know, that's pretty stupid test
        # but at same time I don't know how to test this crap without mocks
        # so I cannot be sure
        self.assertTrue(hasattr(subprocess, 'call'))

    @mock.patch('subprocess.call')
    def test_basic(self, s):
        text = SimpleText('foo bar')
        textedit = TextEditor(text)

        with textedit as t:
            t._file.seek(0, 2)
            t._file.write(' baz')
            t._file.seek(0)
            t.run()
            s.assert_called_with([t._editor, t._file.name])
            result = t.result()

            self.assertEqual(result.text, 'foo bar baz')

    @mock.patch('subprocess.call')
    def test_multirun(self, s):
        text = SimpleText('foo bar')

        textedit = TextEditor(text)
        with self.assertRaises(TextEditorException):
            textedit.run()

        with textedit as t:
            t.run()
            t.run()

            self.assertEqual(t.result().text, 'foo bar')

        self.assertEqual(textedit.result().text, 'foo bar')

    # TODO: test the rest of code
    @mock.patch('subprocess.call')
    def test_edit_specific_file(self, s):
        pass
