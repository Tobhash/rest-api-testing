from models.user import UserModel
from unittest import TestCase

class UserTest(TestCase):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')