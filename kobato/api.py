import requests
import sys
from functools import wraps
from decorating import animated
from requests.exceptions import RequestException, SSLError


def auth_required(function):
    """
    Simple decorator to reduce copypaste
    """
    @wraps(function)
    def f(self, *k, **kw):
        if hasattr(self, '_api'):
            if self._api.is_logged_in():
                return function(self, *k, **kw)
            else:
                print("Terrible news: you need to be logged in to use this action")
                print("Use kobato login command")
                sys.exit(16)
    return f


class ApiException(Exception):
    pass


class Api:
    def __init__(self, config, sysexit=True):
        self._config = config
        self._sysexit = sysexit

    def _auth_token(self):
        return self._config.get("login", {}).get("token", "")

    def _csrf_token(self):
        return self._config.get("login", {}).get("csrf_token", "")

    def clone(self, *, sysexit=True):
        return Api(self._config, sysexit)

    def avatar(self, login=None):
        pass

    def login(self):
        return self._config.get("login", {}).get("login", "")

    def is_logged_in(self):
        res = self._config.get("login", {}).get("is_logged_in", None)

        return res == '1'

    def create_post(self, message, tags=None, private=False):
        if tags is not None and len(tags) == 0:
            tags = None

        if not private:
            private = None
        else:
            private = 'true'

        result = self.request('/post',
                              method='post',
                              animated_text='Pushing into master...',
                              auth=True,
                              csrf=True,
                              data={
                                  'text': message,
                                  'tag': tags,
                                  'private': private
                              })
        return result

    def feed(self, before=None):
        """
        Get user's recent feed.
        Auth required.
        :param int before: defaults to None
        """
        result = self.request('/recent',
                              auth=True,
                              animated_text='Nom-nom...',
                              params={'before': before})

        return result

    def all(self, before=None):
        result = self.request('/all',
                              auth=True,
                              animated_text='Abandon all hope, ye who enter here',
                              params={'before': before})
        return result

    def recent_user(self, login, before=None):
        result = self.request('/blog/{u}'.format(u=login),
                              auth=True,
                              params={'before': before})

        return result

    def comments(self, before=None):
        result = self.request('/comments',
                              auth=True,
                              params={'before': before})

        return result

    def incoming(self, before=None):
        result = self.request('/messages/incoming',
                              auth=True,
                              params={'before': before})

        return result

    def outgoing(self, before=None):
        result = self.request('/messages/outgoing',
                              auth=True,
                              params={'before': before})

        return result

    def counters(self):
        result = self.request('/unread-counters',
                              auth=True)

        return result

    def get_post(self, pid):
        result = self.request('/post/{p}'.format(p=pid),
                              auth=True)

        return result

    def edit_post(self, pid, message, tags=None):
        if tags is not None and len(tags) == 0:
            tags = None

        result = self.request('/post/{p}'.format(p=pid),
                              auth=True,
                              csrf=True,
                              method='put',
                              data={
                                  'text': message,
                                  'tag': tags
                              })

        return result

    def delete_post(self, pid):
        result = self.request('/post/{p}'.format(p=pid),
                              auth=True,
                              csrf=True,
                              method='delete',
                              animated_text='Removing kebab...')

        return result

    def create_comment(self, pid, message, comment_id=None):
        result = self.request('/post/{p}'.format(p=pid),
                              method='post',
                              auth=True,
                              csrf=True,
                              data={
                                  'text': message,
                                  'comment_id': comment_id
                              })

        return result

    def delete_comment(self, pid, comment_id):
        result = self.request('/post/{p}/{i}'.format(p=pid, i=comment_id),
                              method='delete',
                              auth=True,
                              csrf=True,
                              animated_text='Removing microkebab')

        return result

    def rec_post(self, pid, message=None):
        result = self.request('/post/{p}/r'.format(p=pid),
                              method='post',
                              auth=True,
                              csrf=True,
                              data={
                                  'text': message
                              })

        return result

    def unrec_post(self, pid):
        result = self.request('/post/{p}/r'.format(p=pid),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def rec_comment(self, pid, comment_id):
        result = self.request('/post/{p}/{i}/r'.format(p=pid, i=comment_id),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unrec_comment(self, pid, comment_id):
        result = self.request('/post/{p}/{i}/r'.format(p=pid, i=comment_id),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def pin_post(self, pid):
        result = self.request('/post/{p}/pin'.format(p=pid),
                              method='post',
                              auth=True,
                              csrf=True)
        return result

    def unpin_post(self, pid):
        result = self.request('/post/{p}/unpin'.format(p=pid),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def sub_to_post(self, pid):
        result = self.request('/post/{p}/s'.format(p=pid),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unsub_from_post(self, pid):
        result = self.request('/post/{p}/s'.format(p=pid),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def fav_post(self, pid, message=None):
        result = self.request('/post/{p}/b'.format(p=pid),
                              method='post',
                              auth=True,
                              csrf=True,
                              data={'text': message})

    def unfav_post(self, pid):
        result = self.request('/post/{p}/b'.format(p=pid),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def fav_comment(self, pid, comment_id, message=None):
        result = self.request('/post/{p}/{i}/b'.format(p=pid, i=comment_id),
                              method='post',
                              auth=True,
                              csrf=True,
                              data={'text': message})

        return result

    def unfav_comment(self, pid, comment_id):
        result = self.request('/post/{p}/{i}/b'.format(p=pid, i=comment_id),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def user_tags(self, login):
        result = self.request('/tags/{u}'.format(u=login),
                              auth=True)

        return result

    def posts_by_tags(self, tags, login="", before=None):
        result = self.request('/tags/{u}'.format(u=login),
                              auth=True,
                              params={
                                  'before': before,
                                  'tag': tags
                              })

        return result

    def user_info(self, login):
        result = self.request('/user/login/{u}'.format(u=login),
                              auth=True)

        return result

    def self_info(self):
        result = self.request('/me',
                              auth=True)

        return result

    def subscriptions(self, login=None):
        if login is None:
            login = self.login()

        result = self.request('/user/{u}/subscriptions'.format(u=login),
                              auth=True)

        return result

    def subscribers(self, login=None):
        if login is None:
            login = self.login()

        result = self.request('/user/{u}/subscribers'.format(u=login),
                              auth=True)

        return result

    def sub_to_user(self, login):
        result = self.request('/user/s/{u}'.format(u=login),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unsub_from_user(self, login):
        result = self.request('/user/s/{u}'.format(u=login),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def sub_to_user_recs(self, login):
        result = self.request('/user/sr/{u}'.format(u=login),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unsub_from_user_recs(self, login):
        result = self.request('/user/sr/{u}'.format(u=login),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def wl(self):
        result = self.request('/user/wl',
                              auth=True)

        return result

    def wl_user(self, login):
        result = self.request('/user/wl/{u}'.format(u=login),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unwl_user(self, login):
        result = self.request('/user/wl/{u}'.format(u=login),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def bl(self):
        result = self.request('/user/bl',
                              auth=True)

        return result

    def bl_user(self, login):
        result = self.request('/user/bl/{u}'.format(u=login),
                              method='post',
                              auth=True,
                              csrf=True)

        return result

    def unbl_user(self, login):
        result = self.request('/user/bl/{u}'.format(u=login),
                              method='delete',
                              auth=True,
                              csrf=True)

        return result

    def request(self,
                url,
                method='get',  # get|post|put|delete|...
                result='json',  # json|text
                auth=False,
                csrf=False,
                animated_request=True,  # TODO
                animated_text='Doin\' all the things...',
                **kwargs):
        url = 'https://point.im/api' + url
        named_parameters = {}

        if not self._config.get('meta', {}).get('verify_ssl', True):
            named_parameters['verify'] = False

        for key in kwargs:
            named_parameters[key] = kwargs[key]

        if auth or csrf:
            if 'headers' not in named_parameters:
                named_parameters['headers'] = {}

            if auth:
                named_parameters['headers']['Authorization'] = self._auth_token()

            if csrf:
                named_parameters['headers']['X-CSRF'] = self._csrf_token()

        method = getattr(requests, method)

        error = False
        e = None
        output = None
        with animated(animated_text):
            try:
                r = method(url, **named_parameters)
            except SSLError as e_:
                print("ERROR: something wrong with SSL:", type(e_).__name__)
                print("However, you can execute kobato config --set meta.verify_ssl false to suppress this error.")
                error = True
                e = e_
            except RequestException as e_:
                print("ERROR: something went wrong:", type(e_).__name__)
                error = True
                e = e_

        if not error and result == 'json':
            try:
                output = r.json()
            except Exception as e_:
                print("JSON decoding failed:", type(e_).__name__)
                error = True
                e = e_
        elif not error:
            output = r.text

        # I'm really, really sorry for this hack. See #ootjce for more information
        if not error and result == 'json' and 'code' in output and 'message' in output:
            if output['message'] == 'Post not pinned.':
                output['error'] = 'PostNotPinnedError'
            elif output['message'] == 'Post already pinned.':
                output['error'] = 'PostAlreadyPinnedError'

        if not error and result == 'json' and 'error' in output:
            if self._sysexit:
                print("Something went wront, server returned error:", output['error'])
                print("Exiting...")
                sys.exit(63)
            else:
                raise ApiException(output['error'])

        if error:  # something wrong with animated() and sys.exit
            if self._sysexit:
                print("Exiting...")
                sys.exit(127)
            else:
                raise ApiException(e)

        return output
