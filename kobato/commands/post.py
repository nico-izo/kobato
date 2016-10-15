from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.api import auth_required

from kobato.editor.blogpost import BlogPost
from kobato.editor.texteditor import TextEditor
from kobato.template import render
from kobato.prompt import confirm

import sys


class KobatoPost(KobatoBasePlugin):

    def prepare(self, parser):
        parser.add_argument('-t', '--tag', action='append')
        parser.add_argument('--tags', help='Specify multiple tags at once separated by comma')
        parser.add_argument('--draft', default=False, action='store_true', help='Save draft and exit')
        parser.add_argument('-y', '--yes', default=False, action='store_true', help='Don\'t show confirmation')
        parser.add_argument(
            '-f',
            '--fast',
            default=False,
            action='store_true',
            help='Don\'t start editor. Warning: will exit with error if no message text is presented'
        )
        parser.add_argument('-m', '--message')
        parser.add_argument('-p', '--private', default=False, action='store_true', help='Mark post as private')
        parser.add_argument(
            '--stdin',
            default=False,
            action='store_true',
            help='Implies --yes and --fast'
        )
        parser.add_argument('--pin', help='Pin #post or post')
        parser.add_argument('--unpin', help='Unpin #post or post')

    def run(self, args):
        if args['pin']:
            self.pin(args['pin'])
            return

        if args['unpin']:
            self.unpin(args['unpin'])
            return

        post = BlogPost()

        post.private = args['private']

        if args['tag']:
            post.add_tags(args['tag'])  # yes, 'tag' is an array, and 'tags' is a string

        if args['tags']:
            post.add_tags(args['tags'].split(","))

        if args['message']:
            post.text = args['message']

        if args['stdin']:
            # --stdin -> --fast + --yes
            args['fast'] = True
            args['yes'] = True

            tmp = sys.stdin.read()
            tmp_post = BlogPost.decode(tmp)

            post.add_tags(tmp_post.tags)
            post.text = tmp_post.text

        self.post(post, args['fast'], args['yes'], args['draft'])

    @auth_required
    def pin(self, post):
        post_ = post[1:] if post.startswith('#') else post

        print("Pinning post #{}".format(post_))
        self._api.pin_post(post_)

        print('Post #{} was successfully pinned'.format(post_))

    @auth_required
    def unpin(self, post):
        post_ = post[1:] if post.startswith('#') else post

        print('Unpinning post #{}'.format(post_))
        self._api.unpin_post(post_)

        print('Post #{} was successfully unpinned'.format(post_))

    @auth_required
    def post(self, post, fast, yes, draft):

        # do not create ANYTHING if we have yes and fast
        if fast and yes and not draft:
            self._post(post)
            return

        textedit = TextEditor(post)

        with textedit as t:
            if not fast:
                print('Starting text editor...')
                t.run()

            while not yes:
                print('Preview:')
                print(render('pre_post_preview', {'post': t.result()}))

                condition = confirm(text='Done', additional={'e': 'Just give me another try to edit file'})
                if condition == ['y']:
                    break
                elif condition == ['n']:
                    where = t.save()
                    print("\nFinal draft saved as {0}".format(where))
                    return

                t.run()

        post = textedit.result()
        if draft:
            where = textedit.save()
            print("\nFinal draft saved as {0}".format(where))
            print("Draft-only mode, exiting...")
            return

        self._post(post)

    def _post(self, post):
        print("Posting...")

        if not post.text:
            print("ERROR: Post body cannot be empty.")
            sys.exit(1)

        result = self._api.create_post(post.text, post.tags, post.private)

        print("Post #{0} successfully created".format(result['id']))


kobato_plugin_register(
    'post',
    KobatoPost,
    aliases=['p'],
    description='Create and send, pin and unpin your posts',
    default_aliases={
        'pin': 'post --pin {0}',
        'unpin': 'post --unpin {0}'
    }
)
