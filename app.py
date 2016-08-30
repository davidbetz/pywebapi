try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import re
import json
import sys

python_version = int(sys.version[0])

from middleware import Handler

from .general import debug, Strong, parse_querystring
from . import settings
from .raw_middleware import RawMiddleware
from .request_middleware import RequestMiddleware
from .resource_middleware import ResourceMiddleware
from .aws.aws_middleware import AwsMiddleware
from .response_middleware import ResponseMiddleware

def _(env, start_response, middleware):
    # log('env', env)
    path = env['PATH_INFO'].lstrip('/')
    uri = env['REQUEST_URI']

    env_metadata = {}
    for name in env:
        if '.' not in name:
            env_metadata[name] = env[name]

    log_raw_messages = settings.log_raw_messages
    log_raw_messages = log_raw_messages and 'X-UnitTest' not in env

    # log('raw_logger', raw_logger)
    # log('log_raw_messages', log_raw_messages)

    parameters = parse_querystring(uri)
    env['X-parameters'] = parameters

    #++ use nginx for static files
    if path == 'favicon.ico' or path == 'robots.txt':
        yield None

    body = None
    try:
        body_length = int(env.get('CONTENT_LENGTH', '0'))
    except ValueError:
        body_length = 0

    if body_length != 0:
        body = env['wsgi.input'].read(body_length)

    mwhandler = Handler(**{'env': env, 'body': body, 'env_metadata': env_metadata, 'log_raw_messages': log_raw_messages})
    mwhandler.add(RequestMiddleware)
    for wm in middleware:
        mwhandler.add(wm)
    mwhandler.add(ResponseMiddleware)
    mwhandler.execute()

    status = mwhandler["status"]
    result = mwhandler["result"]

    if status == '404':
        start_response("404", [])
        yield [result or '']

    response = mwhandler["response"]
    match_found = mwhandler["match_found"]

    if start_response is not None:
        start_response(status, mwhandler['response_headers'])

    result = result or ''
    yield bytes(result, 'utf-8') if python_version == 3 else result

def web_start(env, start_response):
    return _(env, start_response, [RawMiddleware])

def webapi_start(env, start_response):
    return _(env, start_response, [ResourceMiddleware, AwsMiddleware])
