import unittest

from .general import debug

from json_formatter import JsonFormatter

from formatters import active_formatters

class TestFormatter(unittest.TestCase):
    def test_select_json(self):
        formatter = active_formatters['application/json']
        self.assertIsInstance(formatter, JsonFormatter)

    def test_json_formatter_read(self):
        formatter = JsonFormatter()
        obj = formatter.read('{ "id": 1, "name": "item1", "content": "qwerwqer1" }')
        self.assertEqual(obj['id'], 1)
        self.assertEqual(obj['name'], 'item1')
        self.assertEqual(obj['content'], 'qwerwqer1')

    def test_json_formatter_write(self):
        formatter = JsonFormatter()
        body = formatter.write({ "id": 1, "name": "item1", "content": "qwerwqer1" })
        obj = formatter.read(body)
        self.assertEqual(obj['id'], 1)
        self.assertEqual(obj['name'], 'item1')
        self.assertEqual(obj['content'], 'qwerwqer1')

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureItemRepo)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
