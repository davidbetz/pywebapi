import json

from .formatter_base import FormatterBase

class JsonFormatter(FormatterBase):
    def __init__(self):
        self.core_format = 'application/json'
        self.formats = [self.core_format ]

    def read(self, body):
        try:
            obj = json.loads(body)
        except:
            raise
            obj = None

        return obj

    def write(self, obj, is_pretty = False):
        dumps_args = {}
        if is_pretty:
            dumps_args = {'indent': 4}

        result = json.dumps(obj, **dumps_args)    

        return (result, self.core_format)