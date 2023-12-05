#!/usr/bin/python3
'''Module for Base unit tests.'''
import unittest
from models.base_model import BaseModel, datetime


class TestBaseModel(unittest.TestCase):
    '''Tests the Base class.'''
    def setUp(self):
        '''Imports module, instantiates class'''
        self.base_model = BaseModel()

    def test_initialization(self):
        '''T1: Ensure that the init is correct'''
        self.assertEqual(str(type(self.base_model)),
                         "<class 'models.base_model.BaseModel'>")
        self.assertIsNotNone(self.base_model.id)
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime.datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime.datetime)

    def test_str_representation(self):
        '''T2: Ensure that the string representation is right'''
        str_repr = str(self.base_model)
        self.assertIn(self.base_model.__class__.__name__, str_repr)
        self.assertIn(self.base_model.id, str_repr)

    def test_save_method(self):
        '''T3: Ensure that the save method updates
        the updated_at attribute'''
        initial_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(initial_updated_at, self.base_model.updated_at)

    def test_to_dict_method(self):
        '''T4: Ensure that the to_dict method returns
        a dictionary with expected keys'''
        model_dict = self.base_model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('__class__', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    def test_to_dict_timestamp_format(self):
        '''T5: Ensure that the timestamp in the to_dict
        method is in the correct format'''
        model_dict = self.base_model.to_dict()
        created_at = datetime.datetime \
            .strptime(model_dict['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
        updated_at = datetime.datetime \
            .strptime(model_dict['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
        self.assertIsInstance(created_at, datetime.datetime)
        self.assertIsInstance(updated_at, datetime.datetime)

    def test_init_from_dict(self):
        '''T6: Ensure that an instance can be created from a dictionary'''
        original_model = BaseModel()
        model_dict = original_model.to_dict()
        new_model = BaseModel(**model_dict)
        t1 = original_model.to_dict()
        t2 = new_model.to_dict()
        self.assertEqual(t1, t2)

    def test_init_from_dict_with_args(self):
        '''T7: Ensure that *args is not used when
        creating an instance from a dictionary'''
        original_model = BaseModel()
        model_dict = original_model.to_dict()
        new_model = BaseModel("arg1", "arg2", **model_dict)
        self.assertEqual(original_model.to_dict(), new_model.to_dict())

    def test_init_from_dict_with_datetime_strings(self):
        '''T8: Ensure that datetime strings are
        correctly converted to datetime objects'''
        model_dict = {
            'id': '123',
            'created_at': '2022-01-01T12:34:56.789',
            'updated_at': '2022-01-01T12:34:56.789',
            '__class__': 'BaseModel'
        }
        new_model = BaseModel(**model_dict)
        self.assertIsInstance(new_model.created_at, datetime.datetime)
        self.assertIsInstance(new_model.updated_at, datetime.datetime)


if __name__ == '__main__':
    unittest.main()
