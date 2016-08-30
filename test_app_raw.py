import unittest

from .general import debug

from mock_uwsgi_input import MockUwsgiInput 

from app import webapi_start, web_start

import json

class TestApp(unittest.TestCase):
    def get_env(self, verb, url, content_type=None, http_accept=None, body=None):
        env = {
            'CONTENT_LENGTH': 0,
            'CONTENT_TYPE': 'application/json',
            'DOCUMENT_ROOT': '/usr/share/nginx/html',
            'HTTP_ACCEPT': '*/*',
            'HTTP_CONTENT_LENGTH': '',
            'HTTP_CONTENT_TYPE': 'application/json',
            'HTTP_HOST': '10.1.40.10',
            'HTTP_USER_AGENT': 'curl/7.29.0',
            'PATH_INFO': url,
            'QUERY_STRING': '',
            'REMOTE_ADDR': '10.1.1.42',
            'REMOTE_PORT': '35228',
            'REQUEST_METHOD': verb,
            'REQUEST_URI': url,
            'X-UnitTest': True,
            'SERVER_NAME': '',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1'
        }

        if body is not None:
            env['CONTENT_LENGTH'] = len(body)
            env['wsgi.input'] = MockUwsgiInput(body)

        if content_type is not None:
            env['CONTENT_TYPE'] = content_type

        if http_accept is not None:
            env['HTTP_ACCEPT'] = http_accept

        return env

    def test_raw(self):
        env = self.get_env('GET', '/')
        result = web_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0] 
        self.assertEqual(result, "home page")

    def test_contact(self):
        env = self.get_env('GET', '/contact')
        result = web_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0] 
        self.assertEqual(result, '{"hello": 2}')

    def test_contact(self):
        env = self.get_env('POST', '/contact')
        result = web_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0] 
        self.assertEqual(result, '{"this was": "a post"}')


if __name__ == '__main__':
    unittest.main()
