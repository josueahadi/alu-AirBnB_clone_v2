#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
# import important sqlalchemy modules
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from os import environ

# print format of create_engine
# 'mysql+mysqldb://<username>:<password>@<host>:<port>/<db_name>'
# connect with the mysql database

Base = declarative_base()

storage_type = 'HBNB_TYPE_STORAGE'


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False,
                default=str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of base model class
        Args:
            args: it won't be used
            kwargs: arguments for the constructor of the BaseModel
        Attributes:
            id: unique id generated
            created_at: creation date
            updated_at: updated date
        """
        # Get all attributes from the class (including subclass attributes)
        # All class attributes are valid keys
        valid_keys = set(self.__class__.__dict__.keys())
        valid_keys.update({"id", "created_at", "updated_at"})

        if kwargs:
            for key, value in kwargs.items():
                if key not in valid_keys and key != "__class__":
                    raise KeyError(f"Invalid key: {key}")
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)

            if "id" not in kwargs:
                self.id = str(uuid.uuid4())
            if "created_at" not in kwargs:
                self.created_at = datetime.now()
            if "updated_at" not in kwargs:
                self.updated_at = datetime.now()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

# create all the tables
# Base.metadata.create_all(engine)
