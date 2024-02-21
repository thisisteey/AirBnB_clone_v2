#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(
                String(128),
                nullable=False
        )
        cities = relationship(
                'City',
                cascade='all, delete, delete-orphan',
                backref='state'
        )
    else:
        name = ""

        @property
        def cities(self):
            """Returns the list of City instances with state_id"""
            from models import storage
            cts_in_sts = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    cts_in_sts.append(city)
            return cts_in_sts
