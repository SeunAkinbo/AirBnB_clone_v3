#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        tic = datetime.utcnow()
        inst1 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.utcnow()
        inst2 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


class TestBaseModel_to_dict(unittest.TestCase):
    """Tests for BaseModel.to_dict method"""

    def test_to_dict_type(self):
        """Test that to_dict returns a dictionary"""
        bm = BaseModel()
        self.assertIsInstance(bm.to_dict(), dict)

    def test_to_dict_keys(self):
        """Test that to_dict contains all expected keys"""
        bm = BaseModel()
        expected_keys = ['id', 'created_at', 'updated_at', '__class__']
        self.assertCountEqual(bm.to_dict().keys(), expected_keys)

    def test_to_dict_values(self):
        """Test that to_dict contains correct values"""
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(bm_dict['id'], bm.id)
        self.assertEqual(bm_dict['created_at'], bm.created_at.isoformat())
        self.assertEqual(bm_dict['updated_at'], bm.updated_at.isoformat())
        self.assertEqual(bm_dict['__class__'], 'BaseModel')

    def test_to_dict_datetime_format(self):
        """Test that datetime objects are formatted correctly"""
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertIsInstance(bm_dict['created_at'], str)
        self.assertIsInstance(bm_dict['updated_at'], str)

    def test_to_dict_sa_instance_state(self):
        """Test that _sa_instance_state is removed from the dictionary"""
        bm = BaseModel()
        bm.__dict__['_sa_instance_state'] = 'some_value'
        bm_dict = bm.to_dict()
        self.assertNotIn('_sa_instance_state', bm_dict)

    def test_to_dict_password(self):
        """Test that password is removed from the
        dictionary if storage_t is 'db'
        """
        bm = BaseModel()
        bm.__dict__['password'] = 'secret'
        models.storage_t = 'db'
        bm_dict = bm.to_dict()
        self.assertNotIn('password', bm_dict)


class TestBaseModel_delete(unittest.TestCase):
    """Tests for BaseModel.delete method"""

    def test_delete(self):
        """Test that delete method removes the instance from storage"""
        bm = BaseModel()
        bm_id = bm.id
        bm.delete()
        self.assertIsNone(models.storage.all().get(bm_id))

    def test_delete_nonexistent_instance(self):
        """Test that delete method does not raise an error
        for non-existent instance
        """
        bm = BaseModel()
        bm_id = bm.id
        bm.delete()
        bm.delete()  # Should not raise an error

    @mock.patch('models.storage')
    def test_delete_calls_storage_delete(self, mock_storage):
        """Test that delete method calls storage.delete"""
        bm = BaseModel()
        bm.delete()
        self.assertTrue(mock_storage.delete.called)

    def test_delete_with_password(self):
        """Test that delete method removes the instance
        with password attribute
        """
        bm = BaseModel()
        bm.password = 'secret'
        bm_id = bm.id
        bm.delete()
        self.assertIsNone(models.storage.all().get(bm_id))

    def test_delete_with_sa_instance_state(self):
        """Test that delete method removes the instance
        with _sa_instance_state attribute
        """
        bm = BaseModel()
        bm._sa_instance_state = 'some_value'
        bm_id = bm.id
        bm.delete()
        self.assertIsNone(models.storage.all().get(bm_id))
