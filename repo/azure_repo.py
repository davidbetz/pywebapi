import datetime

from collections import namedtuple

try:
    import azure
    from azure.common import AzureMissingResourceHttpError
    from azure.storage.table import TableService, Entity
except:
    pass

from ..general import debug
from ..settings import azure_storage_key

from ..repo_base import RepoBase

class AzureItemRepo(RepoBase):
    def __init__(self):
        super(AzureItemRepo, self).__init__()
        self.table_service = TableService(account_name = 'content', account_key = azure_storage_key)
        self.table_service.create_table('config')

    def _clean(self, item):
        for k,v in item.iteritems():
            item['Timestamp'] = str(item['Timestamp'])
            # debug.log('k', k)
            # debug.log('v', v)
            if isinstance(v, azure.storage.table.models.EntityProperty):
                item[k] = None

    def all(self):
        item_data = list(self.table_service.query_entities('config'))

        results = []

        for item in item_data:
            self._clean(item)

            results.append(item)

        #debug.log('results', results)

        if len(results) == 0:
            return None

        return results
    
    def get(self, id):
        part_array = id.split('!')

        try:
            item = self.table_service.get_entity('config', part_array[0].lower(), part_array[1].lower())
            self._clean(item)
        except AzureMissingResourceHttpError as ex:
            return None

        # debug.log('id', id)
        # debug.log('item', item)

        '''
        area_config = {}
        for property in vars(item).iteritems():
            key = property[0]

            if key != "etag" and key[0].lower() == key[0]:
                area_config[key] = property[1]
                
        response.body = json.dumps(area_config)
        '''

        return item

    def set_param(self, id, obj, existing_obj = None):
        area = ''
        env = ''

        if id is None:
            raise ValueError('id is required')

        param_array = id.split('!')

        part_count = len(part_array)
        if part_count < 1 or part_count > 2:
            raise ValueError('id is invalid: must be one or two part')
        elif part_count == 1:
            env = 'production'
        else:
            env = part_array[1]

        area = part_array[0]

        item = Entity()
        item.PartitionKey = area.lower()
        item.RowKey = env.lower()

        for n in obj:
            # debug.logline('assigning {}({})'.format(n, obj[n]))
            setattr(item, n, obj[n])

        self.table_service.insert_or_replace_entity('config', item)

        return 0

    def set(self, obj):
        area = ''
        env = ''

        if 'name' in obj:
            area = obj['name']

        if 'environment' in obj:
            env = obj['environment']
        else:
            env = 'production'

        '''
        part_count = len(part_array)
        if part_count < 1 or part_count > 2:
            raise ValueError('id is invalid: must be one or two part')
        elif part_count == 1:
            env = 'production'
        else:
            env = part_array[1]
        area = part_array[0]
        '''

        # debug.log('area', area)
        # debug.log('env', env)

        item = Entity()
        item.PartitionKey = area.lower()
        item.RowKey = env.lower()

        for n in obj:
            # debug.logline('assigning {}({})'.format(n, obj[n]))
            setattr(item, n, obj[n])

        self.table_service.insert_or_replace_entity('config', item)

        return 0
