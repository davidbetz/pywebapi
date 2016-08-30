import unittest

from .general import debug

from .mock_uwsgi_input import MockUwsgiInput 

from .app import webapi_start

import json

import os

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
            'SERVER_NAME': '',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'X-UnitTest': True,
            'HTTP_SIGNATURE': 'GjnmtlSf/BIGQU6I2YNwDDfSDq0uil5cwTdcJXBJofz9yhrQcxqf05rY8EVV1D0JpDPiKvOn0Zu5wmZl/4Qu0+3G1DPbPVaE31G+zHGTvQ1CtYJJ/kyRVp6+hrtfAam0a3//lcm1Uekfjo/GNMIb2Ec+yn3/6ZmYwss4MKOk6iPVLLbYaIgvNGo3BH1pqvnswfTvxVPMVUYlQmFgrVd9qAthEs0auUbr8XW7JgqHuKcQNcXMMS3YYHJC0OsPf7tNp5H5wR3TOTq9KVawpmxhFHRccfbU5ClPUELt6xnG+AkpWMgl++CZK9eLcs4BxHlJQhS1jTHHx66KIGZV+WnusQ==',
            'HTTP_SIGNATURECERTCHAINURL': 'https://s3.amazonaws.com/echo.api/echo-api-cert-3.pem'
        }

        if body is not None:
            env['CONTENT_LENGTH'] = len(body)
            env['wsgi.input'] = MockUwsgiInput(body)

        if content_type is not None:
            env['CONTENT_TYPE'] = content_type

        if http_accept is not None:
            env['HTTP_ACCEPT'] = http_accept

        return env

    def test_aws_skill_get(self):
        """
        POST to /aws/color
        """
        body = '{ "request": { "intent": { "name": "GetValueIntent" }, "locale": "en-US", "requestId": "amzn1.echo-api.request.774a5854-abb9-4662-800a-18bfbfef20d6", "timestamp": "2016-06-30T01:48:40Z", "type": "IntentRequest" }, "session": { "application": { "applicationId": "amzn1.echo-sdk-ams.app.b0e6439a-f5b1-4a47-89fc-12aa0393a265" }, "new": false, "sessionId": "amzn1.echo-api.session.d61f89a4-5b83-4ce3-89e1-e9b9e0ccad06", "attributes": { "numericvalue": 6 }, "user": { "userId": "amzn1.ask.account.AFP3ZWPOS2BGJR7OWJZ3DHPKMOMNWY4AY66FUR7ILBWANIHQN73QGAI77QWXBNMLUMZ7UARUJY4RYW5HVFV7V7YM2PEJXA7TL5DPU3TDFNSIWMNHYXO4WTBAJVBCLKXXAVCROLDGM7GBSPWFRULIBOR25LJWV2WUH2OJY7QB4ZEONROHV2XXL7LHRCZTX2QOVRWBHFEMBES6RDQ" } }, "version": "1.0" }'
        env = self.get_env('GET', '/aws/calc', body=body)
        result = str(webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0])
        debug.log('result', result)
        self.assertTrue(len(result) > 10)


    def _test_aws_skill_substract(self):
        """
        POST to /aws/color
        """
        body = '{ "request": { "intent": { "name": "SubtractIntent", "slots": { "numericvalue": { "name": "numericvalue", "value": "3" } } }, "locale": "en-US", "requestId": "amzn1.echo-api.request.2cf5f769-1078-4b18-acb2-4ce31594229d", "timestamp": "2016-06-30T01:48:22Z", "type": "IntentRequest" }, "session": { "application": { "applicationId": "amzn1.echo-sdk-ams.app.b0e6439a-f5b1-4a47-89fc-12aa0393a265" }, "new": false, "sessionId": "amzn1.echo-api.session.68bbc3cb-2a91-4c2b-ac2a-01dd4621d715", "user": { "userId": "amzn1.ask.account.AFP3ZWPOS2BGJR7OWJZ3DHPKMOMNWY4AY66FUR7ILBWANIHQN73QGAI77QWXBNMLUMZ7UARUJY4RYW5HVFV7V7YM2PEJXA7TL5DPU3TDFNSIWMNHYXO4WTBAJVBCLKXXAVCROLDGM7GBSPWFRULIBOR25LJWV2WUH2OJY7QB4ZEONROHV2XXL7LHRCZTX2QOVRWBHFEMBES6RDQ" } }, "version": "1.0" }'
        env = self.get_env('POST', '/aws/calc', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0]
        # debug.log('result', result)
        self.assertTrue(len(result) > 10)


    def _test_aws_skill_add(self):
        """
        POST to /aws/color
        """
        body = '{ "request": { "intent": { "name": "AddIntent", "slots": { "numericvalue": { "name": "numericvalue", "value": "3" } } }, "locale": "en-US", "requestId": "amzn1.echo-api.request.ccce5595-a367-4189-89ba-8b6604960329", "timestamp": "2016-06-30T01:45:50Z", "type": "IntentRequest" }, "session": { "application": { "applicationId": "amzn1.echo-sdk-ams.app.b0e6439a-f5b1-4a47-89fc-12aa0393a265" }, "new": false, "sessionId": "amzn1.echo-api.session.11795d33-8e2c-4f2a-b777-0dfb6717e127", "user": { "userId": "amzn1.ask.account.AFP3ZWPOS2BGJR7OWJZ3DHPKMOMNWY4AY66FUR7ILBWANIHQN73QGAI77QWXBNMLUMZ7UARUJY4RYW5HVFV7V7YM2PEJXA7TL5DPU3TDFNSIWMNHYXO4WTBAJVBCLKXXAVCROLDGM7GBSPWFRULIBOR25LJWV2WUH2OJY7QB4ZEONROHV2XXL7LHRCZTX2QOVRWBHFEMBES6RDQ" } }, "version": "1.0" }'
        env = self.get_env('POST', '/aws/calc', body=body)
        result = webapi_start(env, lambda status, response_headers: self.assertEqual(status, '200 OK'))[0]
        # debug.log('result', result)
        self.assertTrue(len(result) > 10)


if __name__ == '__main__':
    unittest.main()
