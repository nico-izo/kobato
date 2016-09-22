import unittest
import sys
from unittest import mock
from requests.exceptions import RequestException, SSLError

from kobato.api import Api, ApiException


def dummyReq(json_f=None, e=None):
    """
    simple mock function to replace requests.get/post/delete/put and test api methods
    """
    res = {
        'args': set(),
        'kwargs': {}
    }

    duck = {
        'json': (lambda: {}) if json_f is None else json_f,
        'text': '{}'
    }

    def function(*args, **kwargs):
        res['args'].update(args)
        res['kwargs'].update(kwargs)
        if e is not None:
            raise e

        return type('duck', (object,), duck)

    return (function, res)

class TestApi(unittest.TestCase):
    def test_basic_request(self):
        dummy_config = {}
        api = Api(dummy_config)

        (dummy_post, result) = dummyReq()

        with mock.patch('kobato.api.requests.post', dummy_post):
            api.request('/test',
                        method='post',
                        data={'tag': ['babuf']})

        self.assertEqual(result['args'], set({'https://point.im/api/test'}))
        self.assertEqual(result['kwargs'], {
            'data': {'tag': ['babuf']}
        })

    def test_fail_on_ssl(self):
        api = Api({})

        (dummy_post, _) = dummyReq(e=SSLError())

        with mock.patch('kobato.api.requests.get', dummy_post):
            with self.assertRaises(SystemExit):
                api.request('/me',
                            auth=True)

            api2 = api.clone(sysexit=False)
            with self.assertRaises(ApiException):
                api2.request('/me',
                             auth=True)

    def test_fail_on_request_exception(self):
        api = Api({})

        (dummy_post, _) = dummyReq(e=RequestException)

        with mock.patch('kobato.api.requests.get', dummy_post):
            with self.assertRaises(SystemExit):
                api.request('/me',
                            auth=True)

            api2 = api.clone(sysexit=False)
            with self.assertRaises(ApiException):
                api2.request('/me',
                             auth=True,
                             csrf=True)

    def test_fail_on_json(self):
        api = Api({})

        def raise_():
            raise Exception

        (dummy_post, _) = dummyReq(json_f=raise_)

        with mock.patch('kobato.api.requests.get', dummy_post):
            with self.assertRaises(SystemExit):
                api.request('/me',
                            auth=True)

            api2 = api.clone(sysexit=False)
            with self.assertRaises(ApiException):
                api2.request('/me',
                             auth=True,
                             csrf=True)

    def test_fail_on_errored_response(self):
        api = Api({})

        (dummy_post, _) = dummyReq(json_f=lambda: {'error': 'SomethingError'})

        with mock.patch('kobato.api.requests.get', dummy_post):
            with self.assertRaises(SystemExit):
                api.request('/me',
                            auth=True)

            api2 = api.clone(sysexit=False)
            with self.assertRaises(ApiException):
                api2.request('/me',
                             auth=True,
                             csrf=True)


    def test_create_post(self):
        api = Api({})

        (dummy_post, res) = dummyReq()

        with mock.patch('kobato.api.requests.post', dummy_post):
            api.create_post('new post, lala', ['tag1', 'tag2'])

        self.assertEqual(res['args'], set({'https://point.im/api/post'}))

        self.assertEqual(res['kwargs'], {
            'data': {
                'text': 'new post, lala',
                'tag': ['tag1', 'tag2'],
                'private': None
            },
            'headers': {
                'X-CSRF': '',
                'Authorization': ''
            }
        })
