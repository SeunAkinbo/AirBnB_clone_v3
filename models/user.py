#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """
        Getter method for the password attribute.

        Returns:
            str: The hashed password value.
        """
        return self._password

    @password.setter
    def password(self, value):
        """
        Setter method for the password attribute.

        Hashes the provided password value using MD5 encryption
        before assigning it to the password attribute.

        Args:
            value (str): The password value to be hashed and assigned.
        """
        self._password = hashlib.md5(value.encode('utf8')).hexdigest()
