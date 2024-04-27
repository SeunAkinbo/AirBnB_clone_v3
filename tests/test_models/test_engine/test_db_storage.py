#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)


class TestDBStorageAllNoClass(unittest.TestCase):
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        pass
        new_state = State()
        new_state.name = "Abuja"
        models.storage.new(new_state)
        models.storage.save()
        session = models.storage._DBStorage__session
        retrieved_state = self.storages.get(State, new_state.id)
        self.assertEqual(retrieved_state, new_state)

    def test_all_no_class_empty(self):
        """Test all with no class passed returns empty dict"""
        self.assertEqual(models.storage.all(), {})

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class_two_objs(self):
        """Test all with no class passed returns dict with two added objects"""
        new_state = State()
        new_state.name = 'California'
        models.storage.new(new_state)

        new_city = City()
        new_city.name = 'San Francisco'
        models.storage.new(new_city)

        self.assertEqual(models.storage.all(), {
            new_state.id: new_state,
            new_city.id: new_city
        })


class TestDBStorageNew(unittest.TestCase):
    """Test the new method of the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new_creates_object(self):
        """Test that new creates an object in the database"""
        obj = State(name="California")
        models.storage.new(obj)
        obj_id = obj.id
        all_objs = models.storage.all()
        self.assertIn(obj_id, all_objs)
        self.assertIs(all_objs[obj_id], obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new_assigns_id(self):
        """Test that new assigns an id to the object"""
        obj = State(name="California")
        models.storage.new(obj)
        self.assertIsNotNone(obj.id)


class TestDBStorageSave(unittest.TestCase):
    """Test the save method of the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save_updates_object(self):
        """Test that save updates an existing object"""
        obj = State(name="California")
        models.storage.new(obj)
        obj.name = "Nevada"
        models.storage.save()
        obj_from_db = models.storage.all()[obj.id]
        self.assertEqual(obj_from_db.name, "Nevada")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save_new_object(self):
        """Test that save stores a new object"""
        obj = State(name="California")
        models.storage.save()
        obj_from_db = models.storage.all()[obj.id]
        self.assertEqual(obj, obj_from_db)


class TestDBStorageGet(unittest.TestCase):
    """Test Class for all cases in the DBStorage get method"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_nonexistent_id(self):
        self.assertIsNone(models.storage.get("nonexistent_id"))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_none_id(self):
        self.assertIsNone(models.storage.get(None))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_valid_id(self):
        new_state = State()
        new_state.name = "California"
        models.storage.new(new_state)
        self.assertEqual(models.storage.get(new_state.id), new_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_invalid_id(self):
        self.assertIsNone(models.storage.get(123))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_valid_class(self):
        new_state = State()
        new_state.name = "California"
        models.storage.new(new_state)
        self.assertEqual(models.storage.get(State, new_state.id), new_state)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get_invalid_class(self):
        new_state = State()
        new_state.name = "California"
        models.storage.new(new_state)
        self.assertIsNone(models.storage.get(City, new_state.id))


class TestDBStorageCount(unittest.TestCase):
    """Test Class for all count cases"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_empty(self):
        """Test count with no objects returns 0"""
        self.assertEqual(models.storage.count(), 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_one_object(self):
        """Test count with 1 object returns 1"""
        new_state = State()
        new_state.name = "California"
        models.storage.new(new_state)
        self.assertEqual(models.storage.count(), 1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_multiple_objects(self):
        """Test count with multiple objects returns correct count"""
        new_state = State()
        new_state.name = "California"
        models.storage.new(new_state)

        new_city = City()
        new_city.name = "San Francisco"
        models.storage.new(new_city)

        self.assertEqual(models.storage.count(), 2)
