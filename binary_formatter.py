import json

from .formatter_base import FormatterBase

class BinaryFormatter(FormatterBase):
    def __init__(self):
        self.formats = [
            #'multipart/form-data'
            ##'multipart/form-data; boundary=-------------------------acebdf13572468'
            'application/octet-stream'
            'image/png'
            'image/jpeg'
            'image/gif'
        ]

    def read(self, obj):
        return obj

    def write(self, obj):
        return (obj, '')