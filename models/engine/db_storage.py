#!/usr/bin/python3
"""
this module handles the mysql database storage backend of
our web service
"""


import os
# from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.engine import valid_models

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

def metadata_create_all(engine):
    '''
    all classes that inherit from Base must be
    imported before calling create_all()
    '''
    from models.base_model import Base
    from models.user import User
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.amenity import Amenity
    from models.review import Review
    metadata = Base.metadata
    metadata.create_all(engine)
    return metadata


class DBStorage:
    # __objects = {}
    __engine = None
    __session = None
    __session_generator = None
    __db_url = None

    def __init__(self):
        env = os.environ.get('HBNB_ENV')
        env_user = os.environ.get('HBNB_MYSOL_USER', 'hbnb_dev')
        env_user_pwd = os.environ.get('HBNB_MYSOL_PWD', 'hbnb_dev_pwd')
        env_host = os.environ.get('HBNB_MYSOL_HOST', 'localhost')
        env_db = os.environ.get('HBNB_MYSOL_DB', 'hbnb_dev_db')

        self.__db_url = "mysql+mysqldb://{}:{}@{}/{}".format(
                env_user, env_user_pwd, env_host, env_db)

        self.__engine = create_engine(self.__db_url, pool_pre_ping=True)
        metadata = metadata_create_all(self.__engine)
        self.__session_generator = sessionmaker(
                self.__engine, expire_on_commit=False)
        self.__session_generator = scoped_session(self.__session_generator)
        if env == "test":
            metadata.drop_all(self.__engine)
        self.__session = self.__session_generator()

    def all(self, search_class=None):

        """
        returns a dictionary of objects based on the class given
        """
        # call self.save() first?
        results = {}
        if search_class is None:
            for table in valid_models().values():
                query = self.__session.query(table)
                query = self.construct_dict(query)
                results.update(query)
            return results
        else:
            query = self.__session.query(search_class)
            return self.construct_dict(query)

    def new(self, obj):
        """
        adds a new object to the dictionary object with
        the key string <class>.<id>
        """
        # this might just be enough, since obj would
        # presumably already be mapped to the database table
        self.__session.add(obj)

    def save(self):
        """
        save all changes onto to the database
        """
        self.__session.commit()

    def reload(self):
        """
        expire session and reload a new one
        """
        try:
            self.__session.close()
        except InvalidRequestError:
            pass
        # create all tables in the database (sqlalchemy)
        # use Session.refresh() ?
        metadata_create_all(self.__engine)
        self.__session = self.__session_generator()

    def delete(self, obj=None):
        """
        remove the given object from __objects if it exist within
        if nothing is given do nothing
        """
        if obj is None:
            return
        else:
            ObjClass = type(obj)
            (self
             .__session
             .query(ObjClass)
             .filter(ObjClass.id == obj.id)
             .delete(synchronize_session=False))
            self.save()

    def close(self):
        self.__session.close()

    def construct_key(self, obj):
        """
        helper method to construct key for object dictionary
        """
        return type(obj).__name__ + "." + obj.id

    def construct_dict(self, query_records):
        dictionary = {}
        for entry in query_records:
            key = self.construct_key(entry)
            dictionary.update({key: entry})
        return dictionary

    def get(self, cls, id):
        """
        Returns the object based on the class and its ID,
        or None if not found.
        """
        if cls in classes.values():
            objs = self.all(cls)
            for obj in objs.values():
                if obj.id == id:
                    return obj
        return None

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage.
        """
        if cls is None:
            return len(self.__objects.values())
        else:
            count = 0
            for obj in self.__objects.values():
                if type(obj).__name__ == cls.__name__:
                    count += 1
            return count
