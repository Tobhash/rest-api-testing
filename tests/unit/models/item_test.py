from models.item import ItemModel
from tests.integration.base_test import BaseTest

class ItemTest(BaseTest):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "Error:The name of the item is not equal to the constructor argument")
        self.assertEqual(item.price, 19.99,
                         "Error:The name of the item is not equal to the constructor argument")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)       # because none store was created


    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(item.json(), expected,
                         "The JSON export of the item is incorrect."
                         " Received {}, expected {}".format(item.json(), expected)
                         )
