#!/usr/bin/python3
'''Module for file_storage tests.'''
import unittest
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os


class TestFileStorage(unittest.TestCase):
    '''Tests the FileStorage class.'''
    def setUp(self):
        '''Creates a FileStorage instance'''
        self.file_storage = FileStorage()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.file_storage
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_initialization(self):
        '''T1: Ensure that the FileStorage init is correct'''
        self.assertIsInstance(self.file_storage, FileStorage)
        self.assertEqual(self.file_storage._FileStorage__file_path,
                         "file.json")
        self.assertIsInstance(self.file_storage._FileStorage__objects, dict)

    def test_all_method(self):
        '''T2: Ensure that the all method returns the dictionary __objects'''
        all_objects = self.file_storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertEqual(all_objects, self.file_storage._FileStorage__objects)

    def test_new_method(self):
        '''T3: Ensure that the new method adds an instance to __objects'''
        model = BaseModel()
        self.file_storage.new(model)
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, self.file_storage._FileStorage__objects)
        self.assertEqual(
            self.file_storage._FileStorage__objects[key]
            .to_dict(), model.to_dict())

    def test_save_and_reload_methods(self):
        '''T4: Ensure that save and reload methods work together'''
        model = BaseModel()
        self.file_storage.new(model)
        self.file_storage.save()
        self.file_storage.reload()
        key = f"{model.__class__.__name__}.{model.id}"
        reloaded_model = self.file_storage._FileStorage__objects.get(key)
        self.assertIsNotNone(reloaded_model)
        self.assertEqual(reloaded_model.to_dict(), model.to_dict())

    def test_reload_nonexistent_file(self):
        '''T5: Ensure that reloading from a
        nonexistent file does not raise an error'''
        self.file_storage.reload()  # This should not raise an error

    def test_save_and_reload_multiple_instances(self):
        '''T6: Ensure that multiple instances can be saved and reloaded'''
        model1 = BaseModel()
        model2 = BaseModel()
        key1 = f"{model1.__class__.__name__}.{model1.id}"
        key2 = f"{model2.__class__.__name__}.{model2.id}"

        self.file_storage.new(model1)
        self.file_storage.new(model2)
        self.file_storage.save()
        self.file_storage.reload()

        reloaded_models = self.file_storage.all()
        self.assertIn(key1, reloaded_models)
        self.assertIn(key2, reloaded_models)
        self.assertEqual(reloaded_models[key1].to_dict(), model1.to_dict())
        self.assertEqual(reloaded_models[key2].to_dict(), model2.to_dict())

    def test_save_and_reload_empty_objects(self):
        '''T7: Ensure that saving and
        reloading when __objects is empty works'''
        self.file_storage.save()  # This should not raise an error
        self.file_storage.reload()  # This should not raise an error

    def test_save_and_reload_with_existing_file(self):
        '''T8: Ensure that saving and reloading with an existing file works'''
        model = BaseModel()
        key = f"{model.__class__.__name__}.{model.id}"

        self.file_storage.new(model)
        self.file_storage.save()

        # Create a new FileStorage instance to simulate a different session
        new_file_storage = FileStorage()
        new_file_storage.reload()

        reloaded_model = new_file_storage.all().get(key)
        self.assertIsNotNone(reloaded_model)
        self.assertEqual(reloaded_model.to_dict(), model.to_dict())


if __name__ == '__main__':
    unittest.main()
