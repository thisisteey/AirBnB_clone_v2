#!/usr/bin/python3
"""Unittest for state.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from os import getenv


class test_state(test_basemodel):
    """Unittest for creating the instance of the State class"""

    def __init__(self, *args, **kwargs):
        """Initializing the test class of State"""
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """Test the State 'name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.name), expmsg)
