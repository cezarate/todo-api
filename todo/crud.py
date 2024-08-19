""" This is the crud file

It contains necessary crud operations for the API
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from sqlalchemy import desc
from todo import models, schemas
from todo import logger


def get_many_todos(db: Session, limit: int = 0):
    """ Get all todos
    
    Keyword Arguments:
    db -- The database session

    Returns all todos
    """
    try:
        if limit == 0:
            return db.query(models.Todo).order_by(models.Todo.rank).all()
        return db.query(models.Todo).order_by(models.Todo.rank).limit(limit=limit).all()
    except Exception as e:
        logger.exception(
            "Something went wrong while getting the todo list: %s", e)
        raise


def get_todo(db: Session, todo_id: int):
    """ Get todo given todo_id
    
    Keyword Arguments:
    db -- The database session

    Returns todo if it exists. Raise NoResultFound otherwise
    """
    try:
        if todo := db.query(models.Todo).filter(
            models.Todo.todo_id == todo_id).one():
            return todo
    except NoResultFound as e:
        logger.exception(
            "No result found for the given record: %s", e)
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while getting the todo list: %s", e)
        raise


def get_last_todo(db: Session):
    """ Get todo given todo_id
    
    Keyword Arguments:
    db -- The database session

    Returns todo if it exists. Raise NoResultFound otherwise
    """
    try:
        return db.query(models.Todo).order_by(
            desc(models.Todo.rank)).limit(1).one_or_none()
    except Exception as e:
        logger.exception(
            "Something went wrong while getting the todo list: %s", e)
        raise


def get_first_todo(db: Session):
    """ Get todo given todo_id
    
    Keyword Arguments:
    db -- The database session

    Returns todo if it exists. Raise NoResultFound otherwise
    """
    try:
        return db.query(models.Todo).order_by(
            (models.Todo.rank)).limit(1).one_or_none()
    except Exception as e:
        logger.exception(
            "Something went wrong while getting the todo list: %s", e)
        raise


def add_todo(db: Session, todo: schemas.TodoCreate):
    """ Adds the provided todo to the database
    
    Keyword Arguments:
    db -- The database session
    todo -- The given todo

    Returns the added todo if it does not yet exist in the database.
    Raises IntegrityError otherwise.
    """
    try:
        todo_to_add = models.Todo(
            description=todo.description,
            rank=todo.rank
        )
        db.add(todo_to_add)
        db.commit()

        return todo_to_add
    except IntegrityError as e:
        logger.exception("Duplicate key constraint: %s", e)
        db.rollback()
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while adding the todo: %s", e)
        raise


def update_todo_description(db: Session, todo: schemas.TodoReturn):
    """ Updates the provided todo
    
    Keyword Arguments:
    db -- The database session
    todo -- The given todo

    Updates and returns the todo if it exists in the database.
    Raises NoResultFound otherwise.
    Raises MultipleResultsDFound if multiple records are returned.
    """

    try:
        existing_todo = db.query(models.Todo).filter(
            models.Todo.todo_id == todo.todo_id).one()
        existing_todo.description = todo.description
        db.commit()
        return existing_todo
    except MultipleResultsFound as e:
        logger.exception(
            "Violated duplicate key constraint, check database table for constraints: %s", e)
        raise
    except NoResultFound as e:
        logger.exception(
            "No result found for the given record: %s", e)
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while updating the todo: %s", e)
        raise


def update_todo_rank(db: Session, todo_id: int, new_rank: str):
    """ Updates the provided todo
    
    Keyword Arguments:
    db -- The database session
    todo -- The given todo

    Updates and returns the todo if it exists in the database.
    Raises NoResultFound otherwise.
    Raises MultipleResultsDFound if multiple records are returned.
    """

    try:
        existing_todo = db.query(models.Todo).filter(
            models.Todo.todo_id == todo_id).one()
        existing_todo.rank = new_rank
        db.commit()
        return existing_todo
    except MultipleResultsFound as e:
        logger.exception(
            "Violated duplicate key constraint, check database table for constraints: %s", e)
        raise
    except NoResultFound as e:
        logger.exception(
            "No result found for the given record: %s", e)
        raise
    except Exception as e:
        logger.exception(
            "Something went wrong while updating the todo: %s", e)
        raise


def delete_todo(db: Session, todo_id: int):
    """ Updates the provided todo
    
    Keyword Arguments:
    db -- The database session
    todo -- The given todo

    Updates and returns the todo if it exists in the database.
    Raises NoResultFound otherwise.
    Raises MultipleResultsDFound if multiple records are returned.
    """

    try:
        db.query(models.Todo).filter(models.Todo.todo_id == todo_id).delete()
        db.commit()
    except Exception as e:
        logger.exception(
            "Something went wrong while updating the todo: %s", e)
        raise

            