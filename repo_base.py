from .general import debug

class RepoBase():
    def all(self):
        raise NotImplementedError('all')

    def remove(self, id):
        raise NotImplementedError('remove')
    
    def get(self, id):
        raise NotImplementedError('get')

    def set_param(self, id, obj, existing_obj = None):
        raise NotImplementedError('set_param')

    def set(self, obj):
        raise NotImplementedError('set')