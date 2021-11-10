from models.store import StoreModel
# from app import app
from unittest import TestCase

class StoreTest(TestCase):

    def test_create_store(self):
        store = StoreModel('test')

        self.assertEqual(store.name, 'test',
                         "The name of the store after creation does not equal the constructor argument.")
        
