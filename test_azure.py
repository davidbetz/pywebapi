import unittest

from .general import debug

from repo.azure_repo import AzureItemRepo

class TestAzureItemRepo(unittest.TestCase):
    def test_get(self):
        repo = AzureItemRepo()
        results = repo.get('test!production')
        self.assertEqual(results['PartitionKey'], 'test')

    def test_all(self):
        repo = AzureItemRepo()
        results = repo.all()
        self.assertTrue(len(results) > 0)
        self.assertTrue(len([x for x in results if x['RowKey'] == 'production' and x['PartitionKey'] == 'test']) > 0)

    def test_set(self):
        repo = AzureItemRepo()
        results = repo.set({ 
             'name': 'test',
             'aristotleProvider': 'elastic',
             'assetStorageProvider': 'Azure',
             'cacheProvider': 'Redis',
             'enableAssets': True,
             'labelMode': 'BranchAsLabel',
             'preloadCache': True,
             'searchProvider': 'elastic'
        })
        self.assertEqual(results, 0)

if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAzureItemRepo)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
