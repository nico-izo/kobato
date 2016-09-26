from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.misc import get_data_dir
from kobato.api import auth_required

import subprocess
import argparse
import shutil
import os
import sys

from tempfile import NamedTemporaryFile
from datetime import datetime


def parse_post(post, private=False):
    i = 0
    result = {'text': '', 'tags': [], 'private': private}

    lines = post.splitlines(True)

    for line in lines:
        if i == 0 and line.startswith('*'):
            result['tags'] = [s.strip() for s in line[1:].split(",")]
        else:
            result['text'] += line
        i += 1

    result['text'] = result['text'].strip()

    return result


class KobatoPost(KobatoBasePlugin):

    _post = {
        'tags': [],
        'text': None,
        'private': False
    }

    def prepare(self, parser):
        parser.add_argument('-t', '--tag', action='append')
        parser.add_argument('--tags', help='Specify multiple tags at once separated by comma')
        parser.add_argument('--draft', default=False, action='store_true', help='Save draft and exit')
        parser.add_argument('-y', '--yes', default=False, action='store_true', help='Don\'t show confirmation')
        parser.add_argument('-f', '--fast', default=False, action='store_true', help='Don\'t start editor. Warning: will exit with error if no message text is presented')
        parser.add_argument('-m', '--message')
        parser.add_argument('-p', '--private', default=False, action='store_true', help='Mark post as private')
        parser.add_argument('--list-drafts', default=False, action='store_true', help='Show your drafts')
        parser.add_argument('--stdin', default=False, action='store_true', help='Warning: this option also means --yes and --fast')
        parser.add_argument('--pin', help='Pin #post')
        parser.add_argument('--unpin', help='Unpin #post')

    def run(self, args):
        # TODO: pin post, recommend post, comment, edit post, edit comment

        if args['pin']:
            self.pin(args['pin'])

        if args['unpin']:
            self.unpin(args['unpin'])

        if args['tag']:
            self._post['tags'] += args['tag']
        if args['tags']:
            self._post['tags'] += [s.strip() for s in args['tags'].split(",")]
        if args['message']:
            self._post['text'] = args['message']

        self._post['private'] = args['private']

        if args['stdin']:
            # --stdin -> --fast + --yes
            args['fast'] = True
            args['yes'] = True

            tmp = sys.stdin.read()
            tmp_post = parse_post(tmp, self._post['private'])
            self._post['tags'] = list(set(tmp_post['tags']) | set(self._post['tags']))
            self._post['text'] = tmp_post['text']

        draft = self.runEditor(args)

        self.post(draft)

    @auth_required
    def pin(self, post):
        post_ = post[1:] if post.startswith('#') else post

        print("Pinning post #{}".format(post_))
        res = self._api.pin_post(post_)

        print('Post #{} was successfully pinned'.format(post_))
        sys.exit(0)

    @auth_required
    def unpin(self, post):
        post_ = post[1:] if post.startswith('#') else post

        print('Unpinning post #{}'.format(post_))
        res = self._api.unpin_post(post_)

        print('Post #{} was successfully unpinned'.format(post_))
        sys.exit(0)

    def runEditor(self, args):
        f = NamedTemporaryFile()

        if len(self._post['tags']):
            f.write(bytearray("*" + ", ".join(self._post['tags']) + "\n", 'utf-8'))
        f.write(b"\n")
        if self._post['text']:
            f.write(bytearray(self._post['text'], 'utf-8'))
            f.write(b"\n")
        f.seek(0)

        if not args['fast']:
            print("Starting text editor...")
            subprocess.run(["sensible-editor", f.name])

        out_draft = os.path.join(get_data_dir(), datetime.now().strftime("waifu_draft_%Y-%m-%dT%H_%M_%S.txt"))
        try:
            shutil.copyfile(f.name, out_draft)
        except OSError:
            print("Something went wrong, your draft was not saved. Check permissions on {0}".format(get_data_dir()))
            sys.exit(1)

        f.close()

        with open(out_draft, 'r') as fp:
            self._post = parse_post(fp.read(), self._post['private'])

        self.preview()

        _input = ''
        # usually it false (when you want previews), otherwise skip this part
        while not args['yes']:
            _input = input('Done? [Y|n|e]').lower()
            if _input == 'y' or _input == '':
                break
            elif _input == 'n':
                print("Saved as {0}, exiting...".format(out_draft))
                sys.exit(0)

            print("Starting text editor...")
            subprocess.run(["sensible-editor", out_draft])

            with open(out_draft, 'r') as fp:
                self._post = parse_post(fp.read(), self._post['private'])

            self.preview()

        if args['draft']:
            print("\nFinal draft saved as {0}".format(out_draft))
            print("Draft-only mode, exiting...")
            sys.exit(0)

        return out_draft

    def preview(self):
        print("Preview:")
        print("---{0}---".format("PRIVATE POST" if self._post['private'] else ''))
        if len(self._post['tags']):
            print("*" + ", ".join(self._post['tags']))
            print("")
        if len(self._post['text']):
            print(self._post['text'])
        else:
            print("WARNING: empty post")
        print("---{0}---".format("PRIVATE POST" if self._post['private'] else ''))

    @auth_required
    def post(self, draft):
        print("Reading draft:", draft)

        with open(draft, 'r') as fp:
            self._post = parse_post(fp.read(), self._post['private'])

        def remove_draft():
            print("Removing draft...")
            os.remove(draft)

        print("Posting...")
        if not self._post['text']:
            print("ERROR: Post body cannot be empty.")
            remove_draft()
            sys.exit(1)

        result = self._api.create_post(self._post['text'], self._post['tags'], self._post['private'])

        print("Post #{0} successfully created".format(result['id']))
        remove_draft()

kobato_plugin_register('post', KobatoPost, aliases=['p', 'draft'], description="Create and send new posts, manage drafts and write comments")
