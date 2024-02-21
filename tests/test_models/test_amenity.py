#!/usr/bin/python3
"""Unittest for amenity.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from os import getenv


class test_Amenity(test_basemodel):
    """Unittest for creating instance of the Amenity class"""

    def __init__(self, *args, **kwargs):
        """Initializing the test for Amenity class"""
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """Test Amenity 'name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.name), expmsg)
