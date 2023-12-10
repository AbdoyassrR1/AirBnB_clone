import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    '''Tests the User class.'''
    def setUp(self):
        '''Creates a FileStorage and User instance'''
        self.file_storage = FileStorage()
        self.user = User()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.file_storage
        del self.user
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_user_attributes(self):
        '''Ensure that User class attributes
        are present and initialized correctly'''
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    def test_user_inherits_from_base_model(self):
        '''Ensure that User class inherits from BaseModel'''
        self.assertIsInstance(self.user, BaseModel)

    def test_user_attributes_inherited_from_base_model(self):
        '''Ensure that User inherits attributes from BaseModel'''
        self.assertTrue(hasattr(self.user, 'id'))
        self.assertTrue(hasattr(self.user, 'created_at'))
        self.assertTrue(hasattr(self.user, 'updated_at'))


class TestFileStorageWithUser(unittest.TestCase):
    '''Tests FileStorage with User instances.'''
    def setUp(self):
        '''Creates a FileStorage instance and User instance'''
        self.file_storage = FileStorage()
        self.user = User()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.file_storage
        del self.user
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_user_serialization_and_deserialization(self):
        '''Ensure that User instances can be
        correctly serialized and deserialized'''
        self.user.email = "test@example.com"
        self.user.password = "password123"
        self.user.first_name = "John"
        self.user.last_name = "Doe"

        # Save the User instance to file and reload it
        self.file_storage.new(self.user)
        self.file_storage.save()
        self.file_storage.reload()

        # Check if the reloaded User instance has the same attributes
        reloaded_user = self.file_storage.all().get(f"User.{self.user.id}")
        self.assertIsNotNone(reloaded_user)
        self.assertEqual(reloaded_user.email, "test@example.com")
        self.assertEqual(reloaded_user.password, "password123")
        self.assertEqual(reloaded_user.first_name, "John")
        self.assertEqual(reloaded_user.last_name, "Doe")


if __name__ == '__main__':
    unittest.main()
