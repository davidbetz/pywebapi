import re

from middleware import Middleware

from .general import debug
from .response import Response
from .resources import resources

from .request_handler import RequestHandler

class ResourceMiddleware(Middleware):
    def create(self):
        debug.logline('ResourceMiddleware::create')
        def func(mwa, context):
            debug.logline('ResourceMiddleware::create->func')
            match_found = False

            (env, body, path, verb, content_type, obj) = self.read(context, 'env', 'body', 'path', 'verb', 'content_type', 'obj')

            response = Response()

            for pattern, resource in resources:
                if not match_found:
                    match = re.search(pattern, path)
                    if match is not None:
                        match_found = True
                        input_args = [x for x in match.groups() if x is not None]
                        callback = RequestHandler(resource())
                        if hasattr(callback, verb):
                            if verb in ['get', 'head', 'options', 'delete']:
                                if len(input_args) == 0 and verb == "delete":
                                    response.string_content = '{} requires an id'.format(verb.upper())
                                    response.status_code = 501

                                else:
                                    response = getattr(callback, verb)(env, *input_args)
                            else:
                                if len(input_args) == 0 and verb == "put" or verb == "delete":
                                    response.string_content = '{} requires an id'.format(verb.upper())
                                    response.status_code = 501

                                elif obj is not None:
                                    response = getattr(callback, verb)(env, obj, *input_args)

                                else:
                                    response = getattr(callback, verb)(env, body, *input_args)

    
            self.write(context, **{ 'response': response, 'match_found': match_found})

            return next(mwa)

        return func

