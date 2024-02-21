#!/usr/bin/python3
"""Unittest for user.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from os import getenv


class test_User(test_basemodel):
    """Unittest for creating the instance of User class"""

    def __init__(self, *args, **kwargs):
        """Initializing the User class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Test User 'first_name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.first_name), expmsg)

    def test_last_name(self):
        """Test User 'last_name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.last_name), expmsg)

    def test_email(self):
        """Test User 'email' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.email), expmsg)

    def test_password(self):
        """Test User 'password' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.password), expmsg)
