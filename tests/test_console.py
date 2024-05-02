#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
import inspect
import pep8
import unittest
from unittest.mock import patch, MagicMock
import models
from io import StringIO
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

HBNBCommand = console.HBNBCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


class TestHBNBCommandMethods(unittest.TestCase):
    """Tests for HBNBCommand methods"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_emptyline(self):
        """Test for empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('\n')
            self.assertEqual('', f.getvalue().strip())

    def test_quit(self):
        """Test for quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd('quit'))

    def test_create_no_class(self):
        """Test for create with no class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create')
            self.assertEqual('** class name missing **', f.getvalue().strip())

    def test_create_invalid_class(self):
        """Test for create with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create InvalidClass')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_show_no_class(self):
        """Test for show with no class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show')
            self.assertEqual('** class name missing **', f.getvalue().strip())

    def test_show_invalid_class(self):
        """Test for show with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show InvalidClass')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_show_no_id(self):
        """Test for show with no id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show BaseModel')
            self.assertEqual('** instance id missing **', f.getvalue().strip())

    def test_show_invalid_id(self):
        """Test for show with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('show BaseModel invalid_id')
            self.assertEqual('** no instance found **', f.getvalue().strip())


class TestHBNBCommandUpdateMethod(unittest.TestCase):
    """Tests for HBNBCommand update method"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_update_no_args(self):
        """Test for update with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update')
            self.assertEqual('** class name missing **', f.getvalue().strip())

    def test_update_invalid_class(self):
        """Test for update with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update InvalidClass')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_update_no_id(self):
        """Test for update with no id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update BaseModel')
            self.assertEqual('** instance id missing **', f.getvalue().strip())

    def test_update_invalid_id(self):
        """Test for update with invalid id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('update BaseModel invalid_id')
            self.assertEqual('** no instance found **', f.getvalue().strip())

    def test_update_no_attribute(self):
        """Test for update with no attribute"""
        model = BaseModel()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update BaseModel {model.id}')
            self.assertEqual('** attribute name missing **', f.getvalue().strip())

    def test_update_no_value(self):
        """Test for update with no value"""
        model = BaseModel()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update BaseModel {model.id} name')
            self.assertEqual('** value missing **', f.getvalue().strip())

    def test_update_valid_int(self):
        """Test for update with valid integer value"""
        model = Place()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update Place {model.id} number_rooms 4')
            self.assertEqual(model.number_rooms, 4)

    def test_update_invalid_int(self):
        """Test for update with invalid integer value"""
        model = Place()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update Place {model.id} number_rooms invalid')
            self.assertEqual(model.number_rooms, 0)

    def test_update_valid_float(self):
        """Test for update with valid float value"""
        model = Place()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update Place {model.id} latitude 45.5')
            self.assertEqual(model.latitude, 45.5)

    def test_update_invalid_float(self):
        """Test for update with invalid float value"""
        model = Place()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'update Place {model.id} longitude invalid')
            self.assertEqual(model.longitude, 0.0)


class TestHBNBCommandDestroyMethod(unittest.TestCase):
    """Tests for HBNBCommand destroy method"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_destroy_no_args(self):
        """Test for destroy with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy')
            self.assertEqual('** class name missing **', f.getvalue().strip())

    def test_destroy_invalid_class(self):
        """Test for destroy with invalid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy InvalidClass')
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

    def test_destroy_no_id(self):
        """Test for destroy with no id"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('destroy BaseModel')
            self.assertEqual('** instance id missing **', f.getvalue().strip())

    def test_destroy_invalid_id(self):
        """Test for destroy with invalid id"""
        model = BaseModel()
        model.save()
        invalid_id = 'invalid_id'
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'destroy BaseModel {invalid_id}')
            self.assertEqual('** no instance found **', f.getvalue().strip())

    def test_destroy_valid_instance(self):
        """Test for destroy with valid instance"""
        model = BaseModel()
        model.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f'destroy BaseModel {model.id}')
            self.assertEqual('', f.getvalue().strip())
            self.assertNotIn(model.id, models.storage.all().keys())


class TestHBNBCommandCreateMethod(unittest.TestCase):
    """Tests for HBNBCommand create method"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_create_with_valid_class(self):
        """Test for create with valid class"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            instance_id = f.getvalue().strip()
            self.assertIn(instance_id, models.storage.all().keys())

    def test_create_with_args(self):
        """Test for create with arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel name="Test" number=42')
            instance_id = f.getvalue().strip()
            instance = models.storage.all()[instance_id]
            self.assertEqual(instance.name, "Test")
            self.assertEqual(instance.number, 42)

    def test_create_with_invalid_args(self):
        """Test for create with invalid arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel invalid_arg="value"')
            instance_id = f.getvalue().strip()
            instance = models.storage.all()[instance_id]
            self.assertFalse(hasattr(instance, "invalid_arg"))

    def test_create_with_empty_args(self):
        """Test for create with empty arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel ""')
            instance_id = f.getvalue().strip()
            instance = models.storage.all()[instance_id]
            self.assertEqual(instance.name, "")


class TestKeyValueParser(unittest.TestCase):
    """Tests for _key_value_parser method"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_empty_args(self):
        args = []
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {})

    def test_single_arg_without_equal(self):
        args = ["arg"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {})

    def test_single_arg_with_equal(self):
        args = ["key=value"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key": "value"})

    def test_multiple_args(self):
        args = ["key1=value1", "key2=value2", "key3=value3"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key1": "value1", "key2": "value2", "key3": "value3"})

    def test_arg_with_quoted_value(self):
        args = ["key=\"value with spaces\""]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key": "value with spaces"})

    def test_arg_with_int_value(self):
        args = ["key=42"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key": 42})

    def test_arg_with_float_value(self):
        args = ["key=3.14"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key": 3.14})

    def test_arg_with_invalid_value(self):
        args = ["key=invalid"]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {})

    def test_arg_with_underscore(self):
        args = ["key=\"value_with_underscore\""]
        result = self.console._key_value_parser(args)
        self.assertEqual(result, {"key": "value with underscore"})


class TestHBNBCommandDoEOFMethod(unittest.TestCase):
    """Tests for HBNBCommand do_EOF method"""

    def setUp(self):
        self.console = HBNBCommand()

    def test_do_EOF_no_args(self):
        """Test for do_EOF with no arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            result = self.console.onecmd('EOF')
            self.assertTrue(result)
            self.assertEqual('', f.getvalue().strip())

    def test_do_EOF_with_args(self):
        """Test for do_EOF with arguments"""
        with patch('sys.stdout', new=StringIO()) as f:
            result = self.console.onecmd('EOF arg1 arg2')
            self.assertTrue(result)
            self.assertEqual('', f.getvalue().strip())

    def test_do_EOF_after_other_command(self):
        """Test for do_EOF after another command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create BaseModel')
            result = self.console.onecmd('EOF')
            self.assertTrue(result)
            self.assertEqual('', f.getvalue().strip())

    def test_do_EOF_with_empty_line(self):
        """Test for do_EOF with empty line"""
        with patch('sys.stdout', new=StringIO()) as f:
            result = self.console.onecmd('\n')
            self.assertFalse(result)
            self.assertEqual('', f.getvalue().strip())
            result = self.console.onecmd('EOF')
            self.assertTrue(result)
            self.assertEqual('', f.getvalue().strip())
