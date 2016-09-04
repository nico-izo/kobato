import unittest
import unittest.mock

from kobato.prompt import KobatoPrompt


class TestPrompt(unittest.TestCase):
    def test_basic_input(self):
        p = KobatoPrompt(allow_multiple=False, case_sensitive=False)
        p.add_action('y', help='Yes, submit current post to point.im and remove draft')
        p.add_action('n', help='No, save draft and exit')
        p.add_action('e', help='Run editor to edit post')
        # p.add_help()

        with unittest.mock.patch('builtins.input', lambda: 'y'):
            for i in range(0, 10):
                self.assertEqual(p.input(), ['y'])

        def helper(t=['n', 'd', 'h', '123', '', 'asdasdasdasdasd', '\n\n\n', '``', '\'', '+', 'D']):
            if not len(t):
                raise Exception('This should not happen')

            return t.pop()

        with unittest.mock.patch('builtins.input', helper):
            self.assertEqual(p.input(), ['n'])

        with unittest.mock.patch('builtins.input', lambda: 'N'):
            self.assertEqual(p.input(), ['n'])

    def test_multiple_input(self):
        p = KobatoPrompt(allow_multiple=True, case_sensitive=True)
        p.add_action('r', help='Recommend without comment', conflicts=['R'])
        p.add_action('R', help='Recommend with comment', conflicts=['r'])
        p.add_action('f', help='Favorite post')
        p.add_action('u', help='After all actions unsub from the post')

        # p.add_help()

        with unittest.mock.patch('builtins.input', lambda: 'rfu'):
            res = p.input()
            for c in 'rfu':
                self.assertIn(c, res)

        def helper(t=['Rfu', '+', '"', '213454524', '', 'ASDASD', 'RrRrRrR', 'rR', '']):
            if not len(t):
                raise Exception('This should not happen')

            return t.pop()

        with unittest.mock.patch('builtins.input', helper):
            res = p.input()
            for c in 'Rfu':
                self.assertIn(c, res)
