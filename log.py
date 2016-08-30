import json

try:
    from pymongo import MongoClient
except:
    pass

from .general.debug import kwlog, log, logline, logargs
from . import settings

class LogFactory():
    @staticmethod
    def create(name):
        name = name or ''

        if name.lower() == 'mongo':
            return MongoLog()
        else:
            # abstract is dummy
            return Log()

class Log():
    def save(self, name, json_text):
        pass

class MongoLog(Log):
    def __init__(self):
        self.client = MongoClient(settings.mongo_server)
        self.db = self.client['aws']

    def save(self, name, obj):
        log('saving obj', obj)
        self.db[name].insert_one(obj)
