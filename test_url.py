import unittest

from .general import debug, parse_querystring

class TestUrl(unittest.TestCase):
    def test_parse_querystring(self):
        results = parse_querystring('/?q=1&w=2&e=3')
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0][0], 'q')
        self.assertEqual(results[0][1], '1')
        self.assertEqual(results[1][0], 'w')
        self.assertEqual(results[1][1], '2')
        self.assertEqual(results[2][0], 'e')
        self.assertEqual(results[2][1], '3')

    def test_parse_querystring_without_equals(self):
        results = parse_querystring('/?pretty&q=1&w=2&e=3')
        self.assertEqual(len(results), 4)
        self.assertEqual(results[0][0], 'pretty')
        self.assertEqual(results[0][1], '')
        self.assertEqual(results[1][0], 'q')
        self.assertEqual(results[1][1], '1')
        self.assertEqual(results[2][0], 'w')
        self.assertEqual(results[2][1], '2')
        self.assertEqual(results[3][0], 'e')
        self.assertEqual(results[3][1], '3')

    def test_parse_querystring_has_pretty(self):
        results = parse_querystring('/?pretty&q=1&w=2&e=3')
        self.assertEqual(len(results), 4)
        self.assertEqual([x for x in results if x[0] == 'pretty'][0][0], 'pretty')

if __name__ == '__main__':
    unittest.main()
