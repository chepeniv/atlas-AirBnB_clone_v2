#!/usr/bin/python3
"""
City class that inherits from BaseModel
"""

from models import storage_type
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, Column, String


class City(BaseModel, Base):
    """
    City class that inherits from BaseModel
    Public class attributes:
        state_id: string - empty string: it will be the State.id
        name: string - empty string
    """
    __tablename__ = "cities"

    name = Column(
            String(128),
            nullable=False)

    state_id = Column(
            'State',
            String(60),
            ForeignKey("states.id"),
            nullable=False)

    # likely very unnecessary
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
