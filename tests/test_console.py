#!/usr/bin/python3
'''Module for Console unit tests.'''
import unittest
from unittest.mock import patch
from io import StringIO
import os
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    '''Tests the HBNBCommand class.'''

    def setUp(self):
        '''Creates an instance of HBNBCommand'''
        self.console = HBNBCommand()

    def tearDown(self):
        '''Cleans up resources after tests'''
        del self.console
        # Clean up file.json after each test
        if os.path.exists("file.json"):
            os.remove("file.json")

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_create(self, mock_stdout):
        '''Test create command'''
        self.console.onecmd("create BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertIsNotNone(output)
        self.assertNotEqual("** class name missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_show(self, mock_stdout):
        '''T1: Test show command'''
        self.console.onecmd("show BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_destroy(self, mock_stdout):
        '''T2: Test destroy command'''
        self.console.onecmd("destroy BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertEqual("** instance id missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_all(self, mock_stdout):
        '''T3: Test all command'''
        self.console.onecmd("all BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update(self, mock_stdout):
        '''T4: Test update command'''
        self.console.onecmd("update BaseModel")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_create_with_params(self, mock_stdout):
        '''T5: Test create command with parameters'''
        self.console.onecmd("create BaseModel name=\"John\" age=25")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_show_with_params(self, mock_stdout):
        '''T6: Test show command with parameters'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"show BaseModel {id} name")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_destroy_with_params(self, mock_stdout):
        '''T7: Test destroy command works'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"destroy BaseModel {id}")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_all_with_params(self, mock_stdout):
        '''T8: Test all command with parameters'''
        self.console.onecmd("all BaseModel name=\"John\" age=25")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_with_params(self, mock_stdout):
        '''T9: Test update command with parameters'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"update BaseModel {id} name=\"John\"")
        output = mock_stdout.getvalue().strip()
        self.assertNotEqual("** class name missing **", output)
        self.assertNotEqual("** class doesn't exist **", output)
        self.assertNotEqual("** instance id missing **", output)
        self.assertNotEqual("** no instance found **", output)
        self.assertNotEqual("** attribute name missing **", output)
        self.assertNotEqual("** value missing **", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_invalid_attribute(self, mock_stdout):
        '''T10: Test update command with multiple params'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"update BaseModel {id} email \"aibnb@mail.com\" first_name \"Betty\"")
        self.console.onecmd(f"show BaseModel {id}")
        output = mock_stdout.getvalue().strip()

        self.assertIn("email", output)
        self.assertNotIn("first_name", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_cmd_update_with_different_attribute_types(self, mock_stdout):
        '''T11: Test update command with different attribute types
        [TODO] try it when you have int methods'''
        self.console.onecmd("create BaseModel")
        id = mock_stdout.getvalue().strip()
        self.console.onecmd(f"update BaseModel {id} age 25")
        self.console.onecmd(f"show BaseModel {id}")
        output = mock_stdout.getvalue().strip()

        self.assertIn("age", output)
        self.assertIn("25", output)
        self.assertIsInstance(storage.all()[f"BaseModel.{id}"].age, str)
        # self.assertIsInstance(storage.all()[f"BaseModel.{id}"].age, int)



if __name__ == '__main__':
    unittest.main()
