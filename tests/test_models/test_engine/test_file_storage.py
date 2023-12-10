#!/usr/bin/python3
'''Module for file_storage tests.'''
import unittest
import models
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
import os
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


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

    def test_all(self):
        '''T2.0: test all'''
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        """T2.1: Test All With Arguments"""
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_method(self):
        '''T3: Ensure that the new method adds an instance to __objects'''
        model = BaseModel()
        self.file_storage.new(model)
        key = f"{model.__class__.__name__}.{model.id}"
        self.assertIn(key, self.file_storage._FileStorage__objects)
        self.assertEqual(
            self.file_storage._FileStorage__objects[key]
            .to_dict(), model.to_dict())

    def test_new(self):
        """T3.0: Test New"""
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(base_model)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        self.assertIn("BaseModel." + base_model.id,
                      models.storage.all().keys())
        self.assertIn(base_model, models.storage.all().values())
        self.assertIn("User." + user.id, models.storage.all().keys())
        self.assertIn(user, models.storage.all().values())
        self.assertIn("State." + state.id, models.storage.all().keys())
        self.assertIn(state, models.storage.all().values())
        self.assertIn("Place." + place.id, models.storage.all().keys())
        self.assertIn(place, models.storage.all().values())
        self.assertIn("City." + city.id, models.storage.all().keys())
        self.assertIn(city, models.storage.all().values())
        self.assertIn("Amenity." + amenity.id, models.storage.all().keys())
        self.assertIn(amenity, models.storage.all().values())
        self.assertIn("Review." + review.id, models.storage.all().keys())
        self.assertIn(review, models.storage.all().values())

    def test_new_with_args(self):
        """T3.1: Test New With Arguments"""
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_with_None(self):
        """T3.2: Test New Without AnyThing"""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

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

    def test_save(self):
        """T4.0: Test Save"""
        base_model = BaseModel()
        user = User()
        state = State()
        place = Place()
        city = City()
        amenity = Amenity()
        review = Review()
        models.storage.new(base_model)
        models.storage.new(user)
        models.storage.new(state)
        models.storage.new(place)
        models.storage.new(city)
        models.storage.new(amenity)
        models.storage.new(review)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + base_model.id, save_text)
            self.assertIn("User." + user.id, save_text)
            self.assertIn("State." + state.id, save_text)
            self.assertIn("Place." + place.id, save_text)
            self.assertIn("City." + city.id, save_text)
            self.assertIn("Amenity." + amenity.id, save_text)
            self.assertIn("Review." + review.id, save_text)

    def test_save_with_arg(self):
        """T4.1: Test Save With Arg"""
        with self.assertRaises(TypeError):
            models.storage.save(None)

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

    def test_save_and_reload_with_existing_file_content(self):
        '''T9: Ensure that saving and reloading
        with an existing file and content works'''
        # Create an initial BaseModel instance and save it to file
        model1 = BaseModel()
        key1 = f"{model1.__class__.__name__}.{model1.id}"
        self.file_storage.new(model1)
        self.file_storage.save()

        # Create a new FileStorage instance and reload from the existing file
        new_file_storage = FileStorage()
        new_file_storage.reload()

        # Create a new BaseModel instance and save it to the same file
        model2 = BaseModel()
        key2 = f"{model2.__class__.__name__}.{model2.id}"
        new_file_storage.new(model2)
        new_file_storage.save()

        # Reload the file again and check if both instances are present
        new_file_storage.reload()
        reloaded_models = new_file_storage.all()

        self.assertIn(key1, reloaded_models)
        self.assertIn(key2, reloaded_models)
        self.assertEqual(reloaded_models[key1].to_dict(), model1.to_dict())
        self.assertEqual(reloaded_models[key2].to_dict(), model2.to_dict())

    def test_save_and_reload_with_invalid_json_file(self):
        '''T10: Ensure that reloading with an
        invalid JSON file does not raise an error'''
        # Save an invalid JSON string to the file
        with open(self.file_storage._FileStorage__file_path, 'w') as file:
            file.write("invalid_json_content")

        # Reload the file, this should not raise an error
        self.file_storage.reload()

    def test_save_and_reload_with_corrupted_json_file(self):
        '''T11: Ensure that reloading with a
        corrupted JSON file does not raise an error'''
        # Save a valid JSON string to the file
        model = BaseModel()
        key = f"{model.__class__.__name__}.{model.id}"
        self.file_storage.new(model)
        self.file_storage.save()

        # Corrupt the file by adding extra characters
        with open(self.file_storage._FileStorage__file_path, 'a') as file:
            file.write("extra_characters")

        # Reload the file, this should not raise an error
        self.file_storage.reload()

    def test_save_with_no_objects(self):
        '''T12: Ensure that saving when __objects is empty works'''
        # Clear __objects and save
        self.file_storage._FileStorage__objects = {}
        self.file_storage.save()  # This should not raise an error

    def test_save_and_reload_multiple_instances_same_class(self):
        '''T13: Ensure that multiple instances
        of the same class can be saved and reloaded'''
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

    def test_save_with_non_dict_instance(self):
        '''T14: Ensure that saving an instance
        that does not have to_dict method does not raise an error'''
        class CustomModel:
            pass

        with self.assertRaises(AttributeError):
            custom_model = CustomModel()
            self.file_storage.new(custom_model)
            self.file_storage.save()  # This should not raise an error

            # Ensure that the instance is not saved to the file
            with open(self.file_storage._FileStorage__file_path, 'r') as file:
                content = file.read()
                self.assertNotIn('CustomModel', content)

    def test_new_with_None(self):
        """T15:Test New Without AnyThing"""
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_reload_with_arg(self):
        """T16: Test Reload With Args"""
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_save_with_arg(self):
        """T17: Test Save With Arg"""
        with self.assertRaises(TypeError):
            models.storage.save(None)


if __name__ == '__main__':
    unittest.main()
