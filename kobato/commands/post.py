from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.misc import get_data_dir, kobato_request

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
        parser.add_argument('-d', '--delete', help='Specify #post-id to delete')
        parser.add_argument('-p', '--private', default=False, action='store_true', help='Mark post as private')
        parser.add_argument('--list-drafts', default=False, action='store_true', help='Show your drafts')
        parser.add_argument('--stdin', default=False, action='store_true', help='Warning: this option also means --yes and --fast')
        parser.add_argument('--pin', help='Pin #post')
        parser.add_argument('--unpin', help='Unpin #post')

    def run(self, args):
        # TODO: pin post, recommend post, comment, edit post, edit comment

        if args['delete']:
            print("Deleting post {0}".format(args['delete']))
            if not args['yes']:
                confirm = input("Are you sure? [y|N]")
                if confirm.lower() == 'y':
                    self.delete(args['delete'])
                else:
                    print("Terminated.")
            else:
                self.delete(args['delete'])

            return

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

    def pin(self, post):
        post_ = post[1:] if post.startswith('#') else post

        print("Pinning post #{}".format(post_))
        res = self._api.pin_post(post_)

        print('Post #{} was successfully pinned'.format(post_))
        sys.exit(0)

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

    def post(self, draft):
        print("Reading draft:", draft)

        with open(draft, 'r') as fp:
            self._post = parse_post(fp.read(), self._post['private'])

        print("Posting...")
        if not self._post['text']:
            print("ERROR: Post body cannot be empty.")
            sys.exit(1)

        if not self._config.is_logged_in():
            print("ERROR: You must be logged in")
            sys.exit(1)

        data = {
            'text': self._post['text'],
            'tag': self._post['tags']
        }

        # holy crap, @arts, what the hell? via #ovyszo
        if self._post['private']:
            data['private'] = 'true'

        result = kobato_request('https://point.im/api/post',
                                method='post',
                                ssl_check=True,
                                animated_text='Pushing into master...',
                                headers={
                                    'Authorization': self._config['login']['token'],
                                    'X-CSRF': self._config['login']['csrf_token']
                                },
                                data=data)

        if 'id' in result:
            print("Post #{0} successfully created".format(result['id']))
            print("Removing draft...")
            os.remove(draft)
        else:
            print("Something wrong:", result)
            print("Remember, you still have your draft:", draft)

    def delete(self, post):
        if not self._config.is_logged_in():
            print("ERROR: You must be logged in")
            sys.exit(1)

        post_ = post[1:] if post.startswith('#') else post

        result = kobato_request("https://point.im/api/post/{0}".format(post_),
                                method='delete',
                                ssl_check=True,
                                animated_text='Removing kebab...',
                                headers={
                                    'Authorization': self._config['login']['token'],
                                    'X-CSRF': self._config['login']['csrf_token']
                                })

        if 'error' in result:
            print("Something went wrong:", result['error'])
        else:
            print("Post #{0} has been removed successfully".format(post_))


kobato_plugin_register('post', KobatoPost, aliases=['p', 'draft'], description="Create and send new posts, manage drafts and write comments")
