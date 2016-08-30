from middleware import Middleware

from .formatters import active_formatters

class RequestMiddleware(Middleware):
    def create(self):
        def func(mwa, context):
            env = context["env"]
            
            path = env['PATH_INFO'].lstrip('/')
            verb = env['REQUEST_METHOD'].lower()
            content_type = env['CONTENT_TYPE'].lower()
            http_accept_array = env['HTTP_ACCEPT'].lower().split(',') if 'HTTP_ACCEPT' in env else []

            body = context['body']

            context['path'] = path
            context['verb'] = verb
            context['content_type'] = content_type
            context['http_accept_array'] = http_accept_array

            obj = None
            if body is not None:
                try:
                    formatter = active_formatters[content_type]
                    obj = formatter.read(body)
                except KeyError:
                    pass

            self.write(context, **{ 'path': path, 'verb': verb, 'content_type': content_type, 'http_accept_array': http_accept_array, 'obj': obj })

            return next(mwa)

        return func
