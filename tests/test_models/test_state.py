#!/usr/bin/python3
"""Module for State unit tests."""

import unittest
import models
import os
from models.state import State


class TestState(unittest.TestCase):
    """Test for State"""

    def testin_executable_file(self):
        '''T1: test if file has permissions u+x to execute'''
        # Check for read access
        is_read_true = os.access('models/state.py', os.R_OK)
        self.assertTrue(is_read_true)
        # Check for write access
        is_write_true = os.access('models/state.py', os.W_OK)
        self.assertTrue(is_write_true)
        # Check for execution access
        is_exec_true = os.access('models/state.py', os.X_OK)
        self.assertTrue(is_exec_true)

    def test_init_state(self):
        """T2: test the State (obj)"""
        my_object = State()
        self.assertIsInstance(my_object, State)

    def testing_id(self):
        """T3: testing that id is unique"""
        my_objectId0 = State()
        my_objectId1 = State()
        self.assertNotEqual(my_objectId0.id, my_objectId1.id)

    def testing_str(self):
        '''T4: checking the str format'''
        my_strobject = State()
        dictt = my_strobject.__dict__
        string0 = "[State] ({}) {}".format(my_strobject.id, dictt)
        string1 = str(my_strobject)
        self.assertEqual(string0, string1)

    def testing_save(self):
        """T5: check if date update when save """
        object_upd = State()
        first_update = object_upd.updated_at
        object_upd.save()
        second_update = object_upd.updated_at
        self.assertNotEqual(first_update, second_update)

    def test_to_dict(self):
        '''T6: checking id to dict returns a dic with
        class State, with iso string convertion.'''
        my_modell = State()
        my_dict_modell = my_modell.to_dict()
        self.assertIsInstance(my_dict_modell, dict)
        for key, value in my_dict_modell.items():
            flag = 0
            if my_dict_modell['__class__'] == 'State':
                flag += 1
            self.assertTrue(flag == 1)
        for key, value in my_dict_modell.items():
            if key == 'created_at':
                self.assertIsInstance(value, str)
            if key == 'updated_at':
                self.assertIsInstance(value, str)


if __name__ == '__main__':
    unittest.main()
