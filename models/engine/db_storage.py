#!/usr/bin/python3
"""
This module manages the storage of objects in a MySQL database
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
            'User': User, 'Place': Place, 'Review': Review,
            'State': State, 'City': City, 'Amenity': Amenity
          }


class DBStorage:
    """
    This class manages the storage of objects in a MySQL database.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database connection and sets up the environment.
        """
        env = getenv("HBNB_ENV")
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, pwd, host, db),
                                      pool_pre_ping=True)
        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns a dictionary of all objects, or objects of a specific class.

        Args:
            cls (class): The class to filter objects by.
            If None, all objects are returned.

        Returns:
            dict: A dictionary of objects with their IDs as keys.
        """
        obj_dict = {}
        if cls is None:
            for v in classes.values():
                objects = self.__session.query(v)
                for obj in objects.all():
                    k = obj.__class__.__name__ + '.' + obj.id
                    obj_dict[k] = obj
        else:
            objects = self.__session.query(cls)
            for obj in objects.all():
                k = obj.__class__.__name__ + '.' + obj.id
                obj_dict[k] = obj
        return obj_dict

    def new(self, obj):
        """
        Adds a new object to the current database session.

        Args:
            obj: The object to add.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits changes to the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database session.

        Args:
            obj: The object to delete.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads the database session and creates database tables.
        """
        Base.metadata.create_all(self.__engine)
        s_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(s_factory)
        self.__session = Session

    def close(self):
        """
        Closes the current database session.
        """
        self.__session.remove()
