from .general import debug

from .repo_base import RepoBase

class MemoryRepo(RepoBase):
    def __init__(self):
        debug.logline('!!!!!!!!!!RepoBase.ctor')
        self.items = []

    def cast_id(self, id):
        return id

    def set_identity(self, id):
        self._identity = id
    
    def all(self):
        return self.items

    def remove(self, id):
        self.items = [x for x in self.items if x['id'] != self.cast_id(id)]
    
    def get(self, id):
        item = [x for x in self.items if x['id'] == self.cast_id(id)]

        if len(item) > 0:
            item = item[0]
        else:
            item = None

        return item

    def set_param(self, id, obj, existing_obj = None):
        if obj is None:
            return

        if existing_obj is None:
            existing_obj = self.get(self.cast_id(id))

        is_new = False
        new_id = 0
        if existing_obj is None:
            existing_obj = {}
            if self._identity is None:
                raise ValueError('existing_obj is null and no identity set')

            id = max([self.cast_id(x[self._identity]) for x in self.items]) + 1
            new_id = id
            is_new = True

        for n in obj:
            if n != self._identity:
                #setattr(existing_obj, n, obj[n])
                existing_obj[n] = obj[n]

        if is_new:
            existing_obj[self._identity] = new_id

        #existing_obj['name'] = obj['name']
        #existing_obj['content'] = obj['content']

        if is_new:
            self.items.append(existing_obj)
            return new_id
        else:
            return id

        # debug.log('existing_obj', existing_obj)

    def set(self, obj):
        # debug.logline('repo:set|obj')
        if obj is None:
            return

        is_new = False
        new_obj = {}
        if self._identity is None:
            raise ValueError('no identity set')

        if self.cast_id('1') == '1':
            raise ValueError('cast_id not set; identity cannot be string')

        id = max([int(x[self._identity]) for x in self.items]) + 1

        # debug.log('new_obj', new_obj)
        # debug.log('self._identity', self._identity)
        # debug.log('obj', obj)

        for n in obj:
            if n != self._identity:
                # debug.log('n', n)
                #setattr(new_obj, n, obj[n])
                new_obj[n] = obj[n]

        new_obj[self._identity] = id

        #new_obj['name'] = obj['name']
        #new_obj['content'] = obj['content']

        self.items.append(new_obj)

        return id