import unittest
import sys
from unittest import mock
from unittest.mock import Mock
from requests.exceptions import RequestException, SSLError

from kobato.api import Api, ApiException
import kobato.api

class TestApi(unittest.TestCase):
    @mock.patch('kobato.api.requests.post')
    def test_basic_request(self, post):
        api = Api({})
        api.request('/test',
                    method='post',
                    data={'tag': ['babuf']})

        post.assert_called_once_with('https://point.im/api/test', data={'tag': ['babuf']})

    @mock.patch('kobato.api.requests.get')
    def test_fail_on_ssl(self, get):
        api = Api({})
        get.side_effect = SSLError('Hey hey')

        with self.assertRaises(SystemExit):
            api.request('/me',
                        auth=True)

        api2 = api.clone(sysexit=False)
        with self.assertRaises(ApiException):
            api2.request('/me',
                         auth=True)

    @mock.patch('kobato.api.requests.get')
    def test_fail_on_request_exception(self, get):
        api = Api({})
        get.side_effect = RequestException('I\'m just working here man')

        with self.assertRaises(SystemExit):
            api.request('/me',
                        auth=True)

        api2 = api.clone(sysexit=False)
        with self.assertRaises(ApiException):
            api2.request('/me',
                         auth=True,
                            csrf=True)

    # okay, I have no idea now
    def test_fail_on_json(self):
        pass

    @mock.patch('kobato.api.requests.get')
    def test_fail_on_errored_response(self, get):
        api = Api({})

        get.return_value = {'error': 'SomethingError'}

        with self.assertRaises(SystemExit):
            api.request('/me',
                        auth=True)

        api2 = api.clone(sysexit=False)
        with self.assertRaises(ApiException):
            api2.request('/me',
                         auth=True,
                         csrf=True)


    @mock.patch('kobato.api.requests.post')
    def test_create_post(self, post):
        api = Api({})

        api.create_post('new post, lala', ['tag1', 'tag2'])

        post.assert_called_once_with(
            'https://point.im/api/post',
            data={
                'text': 'new post, lala',
                'tag': ['tag1', 'tag2'],
                'private': None
            },
            headers={
                'X-CSRF': '',
                'Authorization': ''
            }
        )
