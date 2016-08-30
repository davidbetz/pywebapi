from ..general import debug
from ..memory_repo import MemoryRepo

class ItemRepo(MemoryRepo):
    def __init__(self):
        MemoryRepo.__init__(self)
        debug.logline('!!!!!!!!!!ItemRepo.ctor')
        self.set_identity('id')

        self.items = [
            { "id": 1, "name": "item1", "content": "qwerwqer1" },
            { "id": 2, "name": "item2", "content": "qwerwqer2" },
            { "id": 3, "name": "item3", "content": "qwerwqer3" },
            { "id": 4, "name": "item4", "content": "qwerwqer4" },
        ]

    def cast_id(self, id):
        return int(id)