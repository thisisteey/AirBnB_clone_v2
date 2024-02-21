#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity


classes = {"State": State, "City": City, "User": User, "Place": Place,
           "Review": Review, "Amenity": Amenity}


class DBStorage:
    """This class manages storage of hbnb models in MySQL format"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a Database storage instance"""
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        dbname = getenv('HBNB_MYSQL_DB')
        dbenv = getenv('HBNB_ENV')
        dburl = f"mysql+mysqldb://{user}:{passwd}@{host}:3306/{dbname}"
        self.__engine = create_engine(dburl, pool_pre_ping=True)
        if dbenv == 'test':
            Base.metadata.dropall(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in the db storage"""
        objdict = {}
        if cls is None:
            for clsinst in classes.values():
                objinst = self.__session.query(clsinst).all()
                for inst in objinst:
                    key = f"{inst.__class__.__name__}.{inst.id}"
                    objdict[key] = inst
        else:
            objinst = self.__session.query(cls).all()
            for inst in objinst:
                key = f"{inst.__class__.__name__}.{inst.id}"
                objdict[key] = inst
        return objdict

    def new(self, obj):
        """Adds the object to the current database session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as expt:
                self.__session.rollback()
                raise expt

    def save(self):
        """Saves all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """Creates the current database session"""
        Base.metadata.create_all(self.__engine)
        dbsession = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(dbsession)()

    def close(self):
        """Closes the SQLAlchemy storage session"""
        self.__session.close()
