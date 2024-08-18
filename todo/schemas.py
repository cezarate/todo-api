"""This is the schemas file

Contains all schemas for crud operations.
"""

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """This is the base schema for the Todo model"""
    description: str


class TodoCreate(TodoBase):
    """This is the create schema for the Todo model"""
    rank: str


class TodoUpdate(TodoBase):
    """This is the create schema for the Todo model"""
    todo_id: int


class TodoReturn(TodoBase):
    """This is the return schema for the Todo model"""
    todo_id: int
    rank: str

    class Config:
        """To allow orm mode"""
        orm_mode = True
