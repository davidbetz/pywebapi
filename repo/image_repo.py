import os

from ..general import debug
from ..repo_base import RepoBase
from ..settings import image_location

class PictureRepo(RepoBase):
    def __init__(self):
        super(PictureRepo, self).__init__()
        debug.logline('!!!!!!!!!!PictureRepo.ctor')

    def all(self):
        raise NotImplementedError('all')

    def remove(self, id):
        os.remove(os.path.join(image_location, id))
    
    def get(self, id):
        with open(os.path.join(image_location, id), 'rb') as f:
            data = f.read()

        return data

    def set_param(self, id, obj, existing_obj = None):
        with open(os.path.join(image_location, str(id)), 'b+') as out:
            out.write(line)

    def set(self, obj):
        raise NotImplementedError('set')