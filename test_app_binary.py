import unittest

from .general import debug

from mock_uwsgi_input import MockUwsgiInput 

from app import webapi_start

class TestAppBinary(unittest.TestCase):
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
    
    def atest_post_error_bad_body(self):
        pass

    def atest_post_param_new_404(self):
        """
        you cannot POST to /id when the resource does not exist; this is an error
        """
        body = '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'
        env = self.get_env('POST', '/image/5', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '404'))[0]

    def atest_post_param_update(self):
        """
        a POST to /id that does exist will update
        """
        body = '{ "id": 400, "name": "item4", "content": "after test update" }'
        env = self.get_env('POST', '/image/4', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))[0]

    def atest_post(self):
        """
        a POST to / creates a new item
        """
        body = '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'
        env = self.get_env('POST', '/image', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0]
        self.assertEqual(result, '5')
        
    def atest_put_update(self):
        """
        a PUT to /id updates a new item if it exists
        """
        body = '{ "id": 400, "name": "item4", "content": "after test update" }'
        env = self.get_env('PUT', '/image/4', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))[0]

    def atest_put_new(self):
        """
        a PUT to /id creates a new item
        """
        body = '{ "id": 400, "name": "item_new", "content": "after test update" }'
        env = self.get_env('PUT', '/image/4', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '204'))[0]

    def atest_put_error_requires_id(self):
        """
        a PUT requires /id
        """
        body = '{ "id": 400, "name": "item_new", "content": "after test update" }'
        env = self.get_env('PUT', '/image', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '501'))[0]

    def atest_get_bad_accept(self):
        """
        GET on / returns all resources
        """
        env = self.get_env('GET', '/image/4', http_accept='gibberish')
        try:
            webapi_start(env, None)          
        except ValueError:
            pass
        else:
            self.fail('ValueError not raised')
      
    def atest_get_any_http_accept(self):
        """
        GET on / returns all resources
        """
        env = self.get_env('GET', '/image', http_accept='*/*')
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0] 
        self.assertTrue(len(result) > 10)

    def atest_get_param_error(self):
        """
        GET on non existing /id is a 404
        """
        env = self.get_env('GET', '/image/40')
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '404'))[0] 
        self.assertTrue(len(result) == 0)

    def atest_get_param(self):
        """
        GET on existing /id returns the item
        """
        env = self.get_env('GET', '/image/4')
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0] 
        self.assertTrue(len(result) > 10)

if __name__ == '__main__':
    unittest.main()
