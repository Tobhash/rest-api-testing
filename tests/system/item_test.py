from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):

    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context:
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT ' + auth_token

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context:
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)     # 401 - no_auth_header

    def test_get_item_no_found(self):
        with self.app() as client:
            with self.app_context:
                # UserModel('test', '1234').save_to_db()
                # auth_request = client.post('/auth',
                #                            data=json.dumps({'username': 'test', 'password': '1234'}),
                #                            headers={'Content-Type': 'application/json'})
                # auth_token = json.loads(auth_request.data)['access_token']
                header = {'Authorization': self.access_token}
                response = client.get('/item/test', headers=header)
                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Item not found'}, json.loads(response.data))

    def test_get_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                header = {'Authorization': self.access_token}
                response = client.get('/item/test_item', headers=header)
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test_item', 'price': 19.99}, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                response = client.delete('/item/test_item')     # no need for a header
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                item = ItemModel.find_by_name('test')
                print(item)
                # ItemModel('test_item', 19.99, 1).save_to_db()
                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual({'name': 'test', 'price': 19.99}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.post('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test' already exists."}, json.loads(response.data))


    def test_put_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                # ItemModel('test', 19.99, 1).save_to_db()

                response = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                response = client.put('/item/test', data={'price': 19.99, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 19.99)

    def test_item_list(self):
        with self.app() as client:
            with self.app_context:
                StoreModel('test_store').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                response = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]},
                                     json.loads(response.data))