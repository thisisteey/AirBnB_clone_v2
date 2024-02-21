#!/usr/bin/python3
"""Unittest for review.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from os import getenv


class test_review(test_basemodel):
    """Unittest for creating instance of the Review class"""

    def __init__(self, *args, **kwargs):
        """Initializing the test of the Review class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Test Review 'place_id' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.place_id), expmsg)

    def test_user_id(self):
        """Test Review 'user_id' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.user_id), expmsg)

    def test_text(self):
        """Test Review 'text' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.text), expmsg)
