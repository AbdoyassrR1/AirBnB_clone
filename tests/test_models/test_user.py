#!/usr/bin/python3
'''Module for User unit tests.'''
import unittest
from models.user import User
from models.engine.file_storage import FileStorage
import os
from models import storage
from datetime import datetime


class TestUser(unittest.TestCase):
    '''Tests the User class.'''
    def setUp(self):
        '''Imports module, instantiates class'''
        self.user_instance = User()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.user_instance
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_initialization(self):
        '''T1: Ensure that the User class is initialized correctly'''
        self.assertEqual(str(type(self.user_instance)),
                         "<class 'models.user.User'>")
        self.assertIsNotNone(self.user_instance.id)
        self.assertIsInstance(self.user_instance.id, str)
        self.assertIsInstance(self.user_instance.created_at, datetime)
        self.assertIsInstance(self.user_instance.updated_at, datetime)

    def test_str_representation(self):
        '''T2: Ensure that the string representation is
        correct for User class'''
        str_repr = str(self.user_instance)
        self.assertIn(self.user_instance.__class__.__name__, str_repr)
        self.assertIn(self.user_instance.id, str_repr)

    def test_save_method(self):
        '''T3: Ensure that the save method updates the
        updated_at attribute'''
        initial_updated_at = self.user_instance.updated_at
        self.user_instance.save()
        self.assertNotEqual(initial_updated_at, self.user_instance.updated_at)

    def test_to_dict_method(self):
        '''T4: Ensure that the to_dict method returns a
        dictionary with expected keys'''
        user_dict = self.user_instance.to_dict()
        self.assertIsInstance(user_dict, dict)
        self.assertIn('__class__', user_dict)
        self.assertIn('created_at', user_dict)
        self.assertIn('updated_at', user_dict)

    def test_to_dict_timestamp_format(self):
        '''T5: Ensure that the timestamp in the to_dict
        method is in the correct format'''
        user_dict = self.user_instance.to_dict()
        created_at = datetime \
            .strptime(user_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
        updated_at = datetime \
            .strptime(user_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
        self.assertIsInstance(created_at, datetime)
        self.assertIsInstance(updated_at, datetime)

    def test_init_from_dict(self):
        '''T6: Ensure that an instance can be created
        from a dictionary'''
        original_user = User()
        user_dict = original_user.to_dict()
        new_user = User(**user_dict)
        self.assertEqual(original_user.to_dict(), new_user.to_dict())

    def test_init_from_dict_with_args(self):
        '''T7: Ensure that *args is not used when
        creating an instance from a dictionary'''
        original_user = User()
        user_dict = original_user.to_dict()
        new_user = User("arg1", "arg2", **user_dict)
        self.assertEqual(original_user.to_dict(), new_user.to_dict())

    def test_init_from_dict_with_datetime_strings(self):
        '''T8: Ensure that datetime strings are
        correctly converted to datetime objects'''
        user_dict = {
            'id': '123',
            'created_at': '2022-01-01T12:34:56.789',
            'updated_at': '2022-01-01T12:34:56.789',
            '__class__': 'User'
        }
        new_user = User(**user_dict)
        self.assertIsInstance(new_user.created_at, datetime)
        self.assertIsInstance(new_user.updated_at, datetime)

    def test_save_and_reload_instance(self):
        '''T9: Ensure that an instance can be saved and reloaded'''
        original_user = User()
        user_id = original_user.id
        storage.save()
        storage.reload()
        reloaded_user = storage.all().get(f"User.{user_id}")
        self.assertIsNotNone(reloaded_user)
        self.assertEqual(original_user.to_dict(), reloaded_user.to_dict())

    def test_save_and_reload_multiple_instances(self):
        '''T10: Ensure that multiple instances
        can be saved and reloaded'''
        original_user1 = User()
        original_user2 = User()
        user_id1, user_id2 = original_user1.id, original_user2.id
        storage.save()
        storage.reload()
        reloaded_users = storage.all()
        self.assertIn(f"User.{user_id1}", reloaded_users)
        self.assertIn(f"User.{user_id2}", reloaded_users)
        self.assertEqual(original_user1.to_dict(),
                         reloaded_users[f"User.{user_id1}"].to_dict())
        self.assertEqual(original_user2.to_dict(),
                         reloaded_users[f"User.{user_id2}"].to_dict())


if __name__ == '__main__':
    unittest.main()
