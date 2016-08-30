import unittest

import json

from .general import debug
from .mock_uwsgi_input import MockUwsgiInput 
from .app import webapi_start, web_start

class TestApp(unittest.TestCase):
    def get_env(self, verb, url, content_type=None, http_accept=None, body=None):
        env = {
            'CONTENT_LENGTH': 0,
            'CONTENT_TYPE': 'application/json',
            'DOCUMENT_ROOT': '/usr/share/nginx/html',
            'HTTP_ACCEPT': 'application/json',
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
    
    def taco_test_post_error_bad_body(self):
        pass

    def _taco_test_post_param_new_404(self):
        """
        you cannot POST to /id when the resource does not exist; this is an error
        """
        body = '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'
        env = self.get_env('POST', '/item/5', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '404'))[0]

    def taco_test_post_param_update(self):
        """
        a POST to /id that does exist will update
        """
        body = '{ "id": 400, "name": "item4", "content": "after test update" }'
        env = self.get_env('POST', '/item/4', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))
        # webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))
        debug.log('result', result)

    def taco_test_post(self):
        """
        a POST to / creates a new item
        """
        body = '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'
        env = self.get_env('POST', '/item', body=body)
        result = next(webapi_start(env, lambda status, response_headers: self.validate('200 OK', status, response_headers)))
        self.assertEqual(result, b'5')
        
    def taco_test_put_update(self):
        """
        a PUT to /id updates a new item if it exists
        """
        body = '{ "id": 400, "name": "item4", "content": "after test update" }'
        env = self.get_env('PUT', '/item/4', body=body)
        webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))

    def taco_test_put_new(self):
        """
        a PUT to /id creates a new item
        """
        body = '{ "id": 400, "name": "item_new", "content": "after test update" }'
        env = self.get_env('PUT', '/item/4', body=body)
        webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))

    def taco_test_put_error_requires_id(self):
        """
        a PUT requires /id
        """
        body = '{ "id": 400, "name": "item_new", "content": "after test update" }'
        env = self.get_env('PUT', '/item', body=body)
        webapi_start(env, lambda status, response_headers: self.assertEqual(status, '501'))
        
    # def taco_test_delete_error(self):
    #     """
    #     a DELETE requires an id
    #     """
    #     env = self.get_env('DELETE', '/item')
    #     result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '501'))
    #     # debug.log('taco_test_delete_error|result', result)
    #     self.assertEqual(result, b'DELETE requires an id')

    # def taco_test_delete(self):
    #     """
    #     a DELETE to /id deletes the new item
    #     """
    #     env = self.get_env('DELETE', '/item/3')
    #     result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))
    #     self.assertTrue(len(result) == 0)

    # def taco_test_get_bad_accept(self):
    #     """
    #     GET on / returns all resources
    #     """
    #     env = self.get_env('GET', '/item', http_accept='gibberish')
    #     try:
    #         webapi_start(env, None)          
    #     except ValueError:
    #         pass
    #     else:
    #         self.fail('ValueError not raised')
      
    # def taco_test_get_blank_http_accept(self):
    #     """
    #     GET on / returns all resources
    #     """
    #     env = self.get_env('GET', '/item', http_accept='')
    #     result = webapi_start(env, lambda status, response_headers: self.validate('200 OK', status, response_headers))[0] 
    #     self.assertTrue(len(result) > 10)
      
    # def taco_test_get_any_http_accept(self):
    #     """
    #     GET on / returns all resources
    #     """
    #     env = self.get_env('GET', '/item', http_accept='*/*')
    #     result = webapi_start(env, lambda status, response_headers: self.validate('200 OK', status, response_headers))[0] 
    #     self.assertTrue(len(result) > 10)
      
    # def taco_test_get(self):
    #     """
    #     GET on / returns all resources
    #     """
    #     env = self.get_env('GET', '/item')
    #     result = webapi_start(env, lambda status, response_headers: self.validate('200 OK', status, response_headers))[0] 
    #     self.assertTrue(len(result) > 10)

    # def taco_test_get_param_error(self):
    #     """
    #     GET on non existing /id is a 404
    #     """
    #     env = self.get_env('GET', '/item/40')
    #     result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '404'))[0] 
    #     self.assertTrue(len(result) == 0)

    # def test_get_param(self):
    #     """
    #     GET on existing /id returns the item
    #     """
    #     env = self.get_env('GET', '/item/4')
    #     result = webapi_start(env, lambda status, response_headers: self.validate('200 OK', status, response_headers))[0] 
    #     self.assertTrue(len(result) > 10)

    def validate(self, required_status, status, response_headers):
        self.assertEqual(status, required_status)
        if len(response_headers) > 0:
            self.assertEqual([_[1] for _ in response_headers if _[0] == 'Content-Type'][0], 'application/json')

if __name__ == '__main__':
    unittest.main()
