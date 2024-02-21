#!/usr/bin/python3
"""Unittest for place.py is defined"""
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
from os import getenv


class test_Place(test_basemodel):
    """Unittest for creating instance of the Place class"""

    def __init__(self, *args, **kwargs):
        """Initializing the Place test class"""
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """Test Place 'city_id' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.city_id), expmsg)

    def test_user_id(self):
        """Test Place 'user_id' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.user_id), expmsg)

    def test_name(self):
        """Test Place 'name' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.name), expmsg)

    def test_description(self):
        """Test Place 'description' attr"""
        new = self.value()
        expmsg = str if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.description), expmsg)

    def test_number_rooms(self):
        """Test Place 'number_rooms' attr"""
        new = self.value()
        expmsg = int if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.number_rooms), expmsg)

    def test_number_bathrooms(self):
        """Test Place 'number_bathrooms' attr"""
        new = self.value()
        expmsg = int if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.number_bathrooms), expmsg)

    def test_max_guest(self):
        """Test Place 'max_guest' attr"""
        new = self.value()
        expmsg = int if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.max_guest), expmsg)

    def test_price_by_night(self):
        """Test Place 'price_by_night' attr"""
        new = self.value()
        expmsg = int if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.price_by_night), expmsg)

    def test_latitude(self):
        """Test Place 'latitude' attr"""
        new = self.value()
        expmsg = float if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.latitude), expmsg)

    def test_longitude(self):
        """Test Place 'longitude' attr"""
        new = self.value()
        expmsg = float if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.latitude), expmsg)

    def test_amenity_ids(self):
        """Test Place 'amenity_ids' attr"""
        new = self.value()
        expmsg = list if getenv('HBNB_TYPE_STORAGE') != 'db' else type(None)
        self.assertEqual(type(new.amenity_ids), expmsg)
