#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.review import Review
from models.amenity import Amenity


if getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id',
                String(60),
                ForeignKey('places.id'),
                primary_key=True,
                nullable=False
            ),
            Column(
                'amenity_id',
                String(60),
                ForeignKey('amenities.id'),
                primary_key=True,
                nullable=False
            )
    )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(
                String(60),
                ForeignKey('cities.id'),
                nullable=False
        )
        user_id = Column(
                String(60),
                ForeignKey('users.id'),
                nullable=False
        )
        name = Column(
                String(128),
                nullable=False
        )
        description = Column(
                String(1024),
                nullable=True
        )
        number_rooms = Column(
                Integer,
                nullable=False,
                default=0
        )
        number_bathrooms = Column(
                Integer,
                nullable=False,
                default=0
        )
        max_guest = Column(
                Integer,
                nullable=False,
                default=0
        )
        price_by_night = Column(
                Integer,
                nullable=False,
                default=0
        )
        latitude = Column(
                Float,
                nullable=True
        )
        longitude = Column(
                Float,
                nullable=True
        )
        reviews = relationship(
                'Review',
                cascade='all, delete, delete-orphan',
                backref='place'
        )
        amenities = relationship(
                'Amenity',
                secondary=place_amenity,
                viewonly=False,
                backref='place_amenities'
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Returns the list of Review instances with place_id"""
            from models import storage
            allrevs = storage.all(Review)
            revlst = []
            for rev in allrevs.values():
                if rev.place_id == self.id:
                    revlst.append(rev)
            return revlst

        @property
        def amenities(self):
            """Returns the list of Amenity instances based on amenity_ids"""
            from models import storage
            allamtys = storage.all(Amenity)
            amtylst = []
            for amty in allamtys.values():
                if amty.id in self.amenity_ids:
                    amtylst.append(amty)
            return amtylst

        @amenities.setter
        def amenitites(self, amty):
            """Adds Amenity.id to the attr amenity_ids"""
            if amty is not None:
                if isinstance(amty, Amenity):
                    if amty.id not in self.amenity_ids:
                        self.amenity_ids.append(amty.id)
