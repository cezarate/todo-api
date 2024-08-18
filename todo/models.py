""" This is the models file

It contains the models for the database tables for this API.
"""
from sqlalchemy import Column, String, Integer
from todo.database import Base

class Todo(Base):
    """ The model for the Todo Table
    
    Attributes:

    __tablename__ -- The name of the table
    todo_id -- The primary id of the todo table
    description -- The contents of the todo item
    rank -- The lexicographical rank of the item

    longitude and latitude as a pair must be unique.
    """
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
    description = Column(String)
    rank = Column(String, unique=True, index=True)
