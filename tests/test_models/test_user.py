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

    def test_save_and_reload_user_instances(self):
        '''T11: Ensure that User instances can be saved and reloaded'''
        # Create a new User
        original_user1 = User()
        original_user1.first_name = "Betty"
        original_user1.last_name = "Bar"
        original_user1.email = "airbnb@mail.com"
        original_user1.password = "root"
        original_user1.save()

        # Create another new User
        original_user2 = User()
        original_user2.first_name = "John"
        original_user2.email = "airbnb2@mail.com"
        original_user2.password = "root"
        original_user2.save()

        # Reload the data
        storage.save()
        storage.reload()

        # Get the reloaded instances
        reloaded_user1 = storage.all().get(f"User.{original_user1.id}")
        reloaded_user2 = storage.all().get(f"User.{original_user2.id}")

        # Check if the instances are not None
        self.assertIsNotNone(reloaded_user1)
        self.assertIsNotNone(reloaded_user2)

        # Check if the reloaded instances match the original ones
        self.assertEqual(original_user1.to_dict(), reloaded_user1.to_dict())
        self.assertEqual(original_user2.to_dict(), reloaded_user2.to_dict())

    def testing_executable_file(self):
        '''T12: test if file's permissions'''
        # Check for read access
        read_true = os.access('models/user.py', os.R_OK)
        self.assertTrue(read_true)
        # Check for write access
        write_true = os.access('models/user.py', os.W_OK)
        self.assertTrue(write_true)
        # Check for execution access
        exec_true = os.access('models/user.py', os.X_OK)
        self.assertTrue(exec_true)

    def testing_init_Review(self):
        """T13: test if an object is an type Review"""
        my_object = User()
        self.assertIsInstance(my_object, User)

    def testing_id(self):
        """T14: test that id is unique """
        my_objectId = User()
        my_objectId1 = User()
        self.assertNotEqual(my_objectId.id, my_objectId1.id)

    def test_str(self):
        '''T15: check str format'''
        my_strobject = User()
        dictt = my_strobject.__dict__
        string0 = "[User] ({}) {}".format(my_strobject.id, dictt)
        string1 = str(my_strobject)
        self.assertEqual(string0, string1)

    def testing_save(self):
        """T16: check if date tpdate when save """
        object_upd = User()
        first_update = object_upd.updated_at
        object_upd.save()
        second_update = object_upd.updated_at
        self.assertNotEqual(first_update, second_update)

    def testing_to_dict(self):
        '''T17: check if to_dict returns a dictionary,with
        class Review, with iso format'''
        my_modell = User()
        my_dict_modell = my_modell.to_dict()
        self.assertIsInstance(my_dict_modell, dict)
        for key, value in my_dict_modell.items():
            flag = 0
            if my_dict_modell['__class__'] == 'User':
                flag += 1
            self.assertTrue(flag == 1)
        for key, value in my_dict_modell.items():
            if key == 'created_at':
                self.assertIsInstance(value, str)
            if key == 'updated_at':
                self.assertIsInstance(value, str)


if __name__ == '__main__':
    unittest.main()
