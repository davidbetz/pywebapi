import unittest

import json

from .general import debug

from request_handler import RequestHandler as Handler

from repo.item_repo import ItemRepo
"""
curl -i -X POST -H 'Content-Type:application/json' 'http://10.1.40.10/item/5' -d 'asdfasdf'
curl -i -X POST -H 'Content-Type:application/json' 'http://10.1.40.10/item/5' -d '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'
curl -i -X POST -H 'Content-Type:application/json' 'http://10.1.40.10/item/4' -d '{ "id": 400, "name": "item4", "content": "after test update" }'
curl -i -X POST -H 'Content-Type:application/json' 'http://10.1.40.10/item' -d '{ "id": 500, "name": "item5", "content": "qwerwqer5" }'

curl -i -X PUT 'http://10.1.40.10/item/4' -d '{ "id": 400, "name": "item4", "content": "after test update" }'
curl -i -X PUT 'http://10.1.40.10/item' -d '{ "id": 400, "name": "item4", "content": "after test update" }'

curl -i -X DELETE 'http://10.1.40.10/item/3'

curl -i -X GET -H 'Accept:application/json' 'http://10.1.40.10/item'
curl -i -X GET -H 'Accept:application/json' 'http://10.1.40.10/item/40'
curl -i -X GET -H 'Accept:application/json' 'http://10.1.40.10/item/4'

"""

class TestItemRepo(unittest.TestCase):
    '''

    ++ test is pointless with formatters

    def test_post_error_bad_body(self):
        repo = ItemRepo()
        item = Handler(repo)
        response = item.post([], 'asdfasdf', 5)
        self.assertEqual(response.status_code, 400)
    '''

    def test_post_param_new_404(self):
        """
        you cannot POST to /id when the resource does not exist; this is an error
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.post([], json.loads('{ "id": 5, "name": "item5", "content": "qwerwqer5" }'), 5)
        self.assertEqual(response.status_code, 404)

    def test_post_param_update(self):
        """
        a POST to /id that does exist will update
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.post([], json.loads('{ "id": 400, "name": "item4", "content": "after test update" }'), 4)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(repo.all()), 4)

        response = item.get([], 4)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(response.object_content['content'], 'after test update')

    def test_post(self):
        """
        a POST to / creates a new item
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.post([], json.loads('{ "id": 5, "name": "item5", "content": "qwerwqer5" }'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(int(response.string_content), 5)
        self.assertEqual(len(repo.all()), 5)

        response = item.get([], 5)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(response.object_content['content'], 'qwerwqer5')

    def test_put_update(self):
        """
        a PUT to /id updates a new item if it exists
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.put([], json.loads('{ "id": 400, "name": "item4", "content": "after test update" }'), 4)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(repo.all()), 4)

        response = item.get([], 4)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(response.object_content['content'], 'after test update')

    def test_put_new(self):
        """
        a PUT to /id creates a new item
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.put([], json.loads('{ "id": 500, "name": "item5", "content": "qwerwqer5" }'), 5)
        self.assertEqual(int(response.string_content), 5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(repo.all()), 5)

        response = item.get([], 5)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(response.object_content['content'], 'qwerwqer5')

    def test_put_error_requires_id(self):
        """
        a PUT requires /id
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.put([], json.loads('{ "id": 500, "name": "item5", "content": "qwerwqer5" }'))
        self.assertEqual(response.status_code, 501)

    def test_delete_error(self):
        """
        a DELETE requires and id
        """
        repo = ItemRepo()
        item = Handler(repo)
        response = item.delete([], None)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.string_content, "DELETE requires an id")

    def test_delete(self):
        """
        a DELETE to /id deletes the new item
        """
        repo = ItemRepo()
        item = Handler(repo)
        self.assertEqual(len(repo.all()), 4)
        response = item.delete([], 3)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(repo.all()), 3)

    def test_get(self):
        """
        GET on / returns all resources
        """
        item = Handler(ItemRepo())
        response = item.get([])
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(len(response.object_content), 4)

    def test_get_param_error(self):
        """
        GET on non existing /id is a 404
        """
        item = Handler(ItemRepo())
        response = item.get([], 19)
        self.assertEqual(response.status_code, 404)

    def test_get_param(self):
        """
        GET on existing /id returns the item
        """
        item = Handler(ItemRepo())
        response = item.get([], 2)
        self.assertIsNotNone(response.object_content)
        self.assertEqual(response.object_content['name'], 'item2')

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureItemRepo)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
