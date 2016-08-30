import re

from middleware import Middleware

from .response import Response

from .resources import processors

class RawMiddleware(Middleware):
    def create(self):
        def func(mwa, context):
            match_found = False

            (env, body, path, verb, content_type, obj) = self.read(context, 'env', 'body', 'path', 'verb', 'content_type', 'obj')

            response = Response()

            for pattern, processor in processors:
                if not match_found:
                    match = re.search(pattern, path)
                    if match is not None:
                        match_found = True
                        input_args = [x for x in match.groups() if x is not None]
                        callback = processor
                        if hasattr(callback, 'keys'):
                            callback = callback[verb]
                        elif verb != 'get':
                            response.string_content = '{} not supported'.format(verb.upper())
                            response.status_code = 501

                        response = Response()

                        result = callback(**context)
                        if isinstance(result, Response):
                            response = result
                        elif isinstance(result, str):
                            response.string_content = result
                        else:
                            response.object_content = result

                        try:
                            response.status_code = context['status']
                        except:
                            response.status_code = 200
                        
            self.write(context, **{ 'response': response, 'match_found': True })

            return next(mwa)

        return func

