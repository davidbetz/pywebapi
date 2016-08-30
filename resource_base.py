import json

from .general import debug

from .response import Response

class ResourceBase():
    '''
    def get_body_object(self, body_string):
        try:
            obj = json.loads(body_string)
        except:
            obj = None

        return obj
    '''

    def get_arg(self, args, index):
        val = None

        if args is not None and len(args) > 0 and args[0] is not None:
            val = str(args[0])

        return val

    def create_response(self):
        return Response()

    def create_error(self, status_code, message):
        response = self.create_response()
        response.status_code = 500
        response.is_error = True
        if message is not None:
            response.string_content = message
        return response
