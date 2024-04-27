#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")


class TestFileStorageNew(unittest.TestCase):
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new_creates_object(self):
        """Test that new creates an object in __objects"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertIn(obj.id, storage._FileStorage__objects)
        
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage") 
    def test_new_assigns_id(self):
        """Test that new assigns an id to the object"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertIsNotNone(obj.id)

class TestFileStorageSave(unittest.TestCase):
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_updates_file(self):
        """Test that save updates the JSON file"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        obj.name = "California"
        storage.save()
        with open("file.json", "r") as f:
            self.assertIn("California", f.read())

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save_new_and_updates(self):
        """Test save with new object and updating existing""" 
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        obj.name = "California"
        obj2 = State()
        storage.new(obj2)
        storage.save()
        with open("file.json", "r") as f:
            self.assertIn("California", f.read())
            self.assertIn(obj2.id, f.read())

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorageCount(unittest.TestCase):
    """Test count method of FileStorage class"""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_empty(self):
        """Test count with no objects returns 0"""
        storage = FileStorage()
        self.assertEqual(storage.count(), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_one_object(self):
        """Test count with 1 object returns 1"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertEqual(storage.count(), 1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_multiple_objects(self):
        """Test count with multiple objects returns correct count"""
        storage = FileStorage()
        obj1 = State()
        obj2 = City()
        storage.new(obj1)
        storage.new(obj2)
        self.assertEqual(storage.count(), 2)

class TestFileStorageGet(unittest.TestCase):
    """Test get method of FileStorage class"""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_valid_id(self):
        """Test get with valid id returns object"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertEqual(storage.get(obj.id), obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_invalid_id(self):
        """Test get with invalid id returns None"""
        storage = FileStorage()
        self.assertIsNone(storage.get("invalid"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_valid_class(self):
        """Test get with valid class returns object"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertEqual(storage.get(State, obj.id), obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_invalid_class(self):
        """Test get with invalid class returns None"""
        storage = FileStorage()
        obj = State()
        storage.new(obj)
        self.assertIsNone(storage.get(City, obj.id))
        self.assertIsNone(storage.get(City, obj.id))

    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
