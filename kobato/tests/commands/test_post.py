import unittest

from kobato.commands.post import KobatoPost
from unittest.mock import Mock


# TODO FIXME: yes, I know, that's a crap
# I just don't want to edit multiple things at the same time, so I'll rewrite it
def prepare_arguments(**kwargs):
    args = {
        'tag': None,
        'tags': None,
        'draft': False,
        'fast': False,
        'yes': False,
        'message': None,
        'private': False,
        'stdin': False,
        'pin': None,
        'unpin': None
    }

    for argument in args:
        args[argument] = kwargs.get(argument, args[argument])

    return args


class TestKobatoPost(unittest.TestCase):

    @unittest.mock.patch('kobato.commands.post.confirm')
    @unittest.mock.patch('kobato.editor.texteditor.TextEditor.run')
    def test_basic_post(self, run_editor, confirm):
        config = {}
        post = KobatoPost(config)
        post._api = Mock()

        confirm.return_value = ['y']
        with self.assertRaises(SystemExit):
            post.run(prepare_arguments())

        post._api.reset_mock()

        post._api.create_post.return_value = {'id': 'foobar'}
        post.run(prepare_arguments(
            message='foo bar',
            tag=['tag 1', 'tag 2'],
            yes=True,
            fast=True
        ))

        # fun thing that I shouldn't do anything about this
        post._api.is_logged_in.assert_called_once_with()

        post._api.create_post.assert_called_once_with('foo bar', ['tag 1', 'tag 2'], False)

    def test_fail_actions_without_login(self):
        post = KobatoPost({})
        post._api = Mock()

        post._api.is_logged_in.return_value = False

        with self.assertRaises(SystemExit):
            post.run(prepare_arguments(yes=True, fast=True, message='test'))

        with self.assertRaises(SystemExit):
            post.run(prepare_arguments(pin='post'))

        with self.assertRaises(SystemExit):
            post.run(prepare_arguments(unpin='post'))

    @unittest.mock.patch('kobato.commands.post.confirm')
    @unittest.mock.patch('kobato.editor.texteditor.TextEditor.run')
    @unittest.mock.patch('kobato.editor.texteditor.TextEditor.save')
    def test_draft_mode(self, save, run_editor, confirm):
        post = KobatoPost({})
        post._api = Mock()

        confirm.return_value = ['y']

        # just draft
        post.run(prepare_arguments(
            draft=True,
            message='foo',
            tag=['tag 1', 'tag 2']
        ))

        post._api.create_post.assert_not_called()
        run_editor.assert_called_once_with()
        save.assert_called_once_with()

        post._api.reset_mock()
        run_editor.reset_mock()
        save.reset_mock()

        # draft with --fast
        post.run(prepare_arguments(
            draft=True,
            fast=True,
            message='foo',
            tag=['tag 1']
        ))

        post._api.create_post.assert_not_called()
        run_editor.assert_not_called()
        save.assert_called_once_with()

        post._api.reset_mock()
        run_editor.reset_mock()
        save.reset_mock()

        confirm.reset_mock()

        # draft with --fast and --yes
        post.run(prepare_arguments(
            draft=True,
            fast=True,
            yes=True,
            message='foo',
            tag=['tag 1']
        ))

        post._api.create_post.assert_not_called()
        run_editor.assert_not_called()
        confirm.assert_not_called()
        save.assert_called_once_with()

        post._api.reset_mock()
        run_editor.reset_mock()
        save.reset_mock()

        # draft with --yes
        post.run(prepare_arguments(
            draft=True,
            yes=True,
            message='foo',
            tag=['tag 1']
        ))

        post._api.create_post.assert_not_called()
        run_editor.assert_called_once_with()
        confirm.assert_not_called()
        save.assert_called_once_with()

        post._api.reset_mock()
        run_editor.reset_mock()
        save.reset_mock()
        confirm.reset_mock()

        confirm.return_value = ['n']
        # not a draft, but save
        post.run(prepare_arguments(
            fast=True,
            message='foo',
            tag=['tag 1']
        ))

        post._api.create_post.assert_not_called()
        run_editor.assert_not_called()
        save.assert_called_once_with()

    def test_pin(self):
        post = KobatoPost({})
        post._api = Mock()

        post.run(prepare_arguments(
            pin='postid'
        ))

        post._api.pin_post.assert_called_once_with('postid')

        post._api.pin_post.reset_mock()

        post.run(prepare_arguments(
            pin='#postid2'
        ))

        post._api.pin_post.assert_called_once_with('postid2')

    def test_unpin(self):
        post = KobatoPost({})
        post._api = Mock()

        post.run(prepare_arguments(
            unpin='postid'
        ))

        post._api.unpin_post.assert_called_once_with('postid')

        post._api.unpin_post.reset_mock()

        post.run(prepare_arguments(
            unpin='#postid2'
        ))

        post._api.unpin_post.assert_called_once_with('postid2')

    def test_tags_and_tag_parameter(self):
        post = KobatoPost({})
        post._api = Mock()

        post._api.create_post.return_value = {'id': 'some_post_id'}
        post.run(prepare_arguments(
            fast=True,
            yes=True,
            tags='tag 1,     t a g 2 \t\t\n, tag 3',
            tag=['tag 0'],
            message='foo'
        ))

        post._api.create_post.assert_called_with('foo', ['tag 0', 'tag 1', 't a g 2', 'tag 3'], False)

    def test_private(self):
        post = KobatoPost({})
        post._api = Mock()

        post._api.create_post.return_value = {'id': 'some_post_id'}
        post.run(prepare_arguments(
            fast=True,
            yes=True,
            private=True,
            tags='tag 1',
            message='foo'
        ))

        post._api.create_post.assert_called_with('foo', ['tag 1'], True)

