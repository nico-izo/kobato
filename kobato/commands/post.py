from kobato.plugin import KobatoBasePlugin, kobato_plugin_register
from kobato.misc import get_data_dir
from kobato.config import Config, config_sync, is_logged_in

import subprocess
import argparse
import shutil
import os
import sys
import requests

from tempfile import NamedTemporaryFile
from datetime import datetime
from decorating import animated

class KobatoPost(KobatoBasePlugin):
    
    _post = {
        'tags': [],
        'text': None,
        'private': False
    }
    
    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-t', '--tag', action='append')
        parser.add_argument('--tags')
        parser.add_argument('--draft', default=False, action='store_true')
        parser.add_argument('-y', '--yes', default=False, action='store_true')
        parser.add_argument('-f', '--fast', default=False, action='store_true', help='Don\'t start editor. Warning: will exit with error if no message text is presented')
        parser.add_argument('-m', '--message')
        parser.add_argument('-d', '--delete')
        parser.add_argument('-p', '--private', default=False, action='store_true')
        parser.add_argument('--list-drafts', default=False, action='store_true')
        
        # TODO: pin post, recommend post, comment, edit post, edit comment
        
        self._parsed_args = vars(parser.parse_args(self._args))
        
        if self._parsed_args['delete']:
            print("Deleting post {0}".format(self._parsed_args['delete']))
            if 'yes' not in self._parsed_args:
                confirm = input("Are you sure? [y|N]")
                if confirm.lower() == 'y':
                    self.delete(self._parsed_args['delete'])
            else:
                self.delete(self._parsed_args['delete'])
                
            return
                
        
        if self._parsed_args['tag']:
            self._post['tags'] += self._parsed_args['tag']
        if self._parsed_args['tags']:
            self._post['tags'] += [s.strip() for s in self._parsed_args['tags'].split(",")]
        if self._parsed_args['message']:
            self._post['text'] = self._parsed_args['message']
        self._post['private'] = self._parsed_args['private']
        
        
        self.runEditor()
        
        self.post()

    def runEditor(self):
        f = NamedTemporaryFile()
        f.write(bytearray("*" + ", ".join(self._post['tags']) + "\n", 'utf-8'))
        f.write(b"\n")
        if self._post['text']:
            f.write(bytearray(self._post['text'], 'utf-8'))
        f.seek(0)
        
        if not self._parsed_args['fast']:
            print("Starting text editor...")
            subprocess.run(["sensible-editor", f.name])
        
        out_draft = os.path.join(get_data_dir(), datetime.now().strftime("waifu_draft_%Y-%m-%dT%H_%M_%S.txt"))
        try:
            shutil.copyfile(f.name, out_draft)
        except OSError:
            print("Something went wrong, your draft was not saved. Check permissions on {0}".format(get_data_dir))
            sys.exit(1)
        
        f.close()
        self._post = self.parse_post(out_draft)
        self.preview()
        
        _input = ''
        # usually it false (when you want previews), otherwise skip this part
        while not self._parsed_args['yes']:
            _input = input('Done? [Y|n|e]').lower()
            if _input == 'y' or _input == '':
                break
            elif _input == 'n':
                print("Saved as {0}, exiting...".format(out_draft))
                sys.exit(0)
            
            print("Starting text editor...")
            subprocess.run(["sensible-editor", out_draft])
            self._post = self.parse_post(out_draft)
            self.preview()
        
        if self._parsed_args['draft']:
            print("Draft-only mode, exiting...")
            sys.exit(0)
        
        self._post = self.parse_post(out_draft)
        
    def preview(self):
        print("Preview:")
        print("---{0}---".format("PRIVATE POST" if self._post['private'] else ''))
        print("*" + ", ".join(self._post['tags']))
        print(self._post['text'])
        print("---{0}---".format("PRIVATE POST" if self._post['private'] else ''))

    def parse_post(self, filename):
        i = 0
        post = {'text': ''}
        for line in open(filename, encoding = "UTF-8"):
            if i == 0 and line.startswith('*'):
                post['tags'] = [s.strip() for s in line[1:].split(",")]
            else:
                post['text'] += line
            i += 1
                
        post['text'].strip()
        
        post['private'] = self._post['private']
        return post

    @animated('Pushing into master...')
    def post(self):
        print("Posting...")
        if not self._post['text']:
            print("ERROR: Post body cannot be empty.")
            return

        if not is_logged_in():
            print("ERROR: You must be logged in")
            return
        
        data = {
            'text': self._post['text'],
            'tag': self._post['tags']
        }
        
        # holy crap, @arts, what the hell? via #ovyszo
        if self._post['private']:
            data['private'] = 'true'
        
        r = requests.post(
            "https://point.im/api/post", 
            headers = {
                'Authorization': Config['login']['token'], 
                'X-CSRF': Config['login']['csrf_token']
                },
            data = data
            )
        
        try:
            result = r.json()
            if 'id' in result:
                print("Post #{0} successfully created".format(result['id']))
            else:
                print("Something wrong")
        except Exception:
            print("Something TERRIBLY wrong")
    
    @animated('Removing kebab...')
    def delete(self, post):
        if not is_logged_in():
            print("ERROR: You must be logged in")
            return
    
        post_ = post[1:] if post.startswith('#') else post
        r = requests.delete(
            "https://point.im/api/post/{0}".format(post_), 
            headers = {
                'Authorization': Config['login']['token'], 
                'X-CSRF': Config['login']['csrf_token']
                }
            )
        
        try:
            res = r.json()
            if 'error' in res:
                print("Something went wrong:", res['error'])
            else:
                print("Post {0} has been removed successfully".format(post))
        except Exception:
            print("JSON parsing failed")


kobato_plugin_register('post', KobatoPost, aliases = ('p', 'draft'), description = "Create and send new posts, manage drafts and write comments")
