#!/usr/bin/python3
"""Unittest for city.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.city import City
from os import getenv


class test_City(test_basemodel):
    """Unittest for creating the instance of the City class"""

    def __init__(self, *args, **kwargs):
        """Initializing the test class of City"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Test City 'state_id' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.state_id), expmsg)

    def test_name(self):
        """Test City 'name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.name), expmsg)
