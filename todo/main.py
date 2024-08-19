""" This is the main file

It contains the routes and exception handling.
"""
from typing import Optional
from fastapi import Depends, FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, MultipleResultsFound, NoResultFound
from todo import crud, models, schemas, LEXORANK_STEP
from todo.database import SessionLocal, engine

from lexorank.lexorank import Bucket, parse, middle, between

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """ Creates and yields the database session. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """ Handles all raised IntegrityErrors.

    Returns error code 400, Duplicate key constraint violated 
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": [{"msg": "Duplicate key constraint violated"}]}),
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """ Handles all raised IntegrityErrors.

    Returns error code 400, Duplicate key constraint violated 
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": [{"msg": f"Invalid data format: {exc}"}]}),
    )

@app.exception_handler(MultipleResultsFound)
async def multiple_results_exception_handler(request: Request, exc: MultipleResultsFound):
    """ Handles all raised MultipleResultsFound.

    Returns error code 500, Internal Server Error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": [{"msg": "Internal Server Error"}]}),
    )

@app.exception_handler(NoResultFound)
async def no_result_exception_handler(request: Request, exc: NoResultFound):
    """ Handles all raised NoResultFound.

    Returns error code 404, Record not found
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"detail": [{"msg": "Record not found"}]}),
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """ Handles unhandled raised exceptions
    
    Returns error code 500, Internal Server Error
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": [{"msg": "Internal Server Error"}]}),
    )


@app.get("/todo/", response_model=list[schemas.TodoReturn])
def get_all_todos(db: Session = Depends(get_db)):
    """ A GET request for returning all todos
    
    Keyword Arguments:
    db -- The database session

    Returns all todos if successful.
    """
    return crud.get_many_todos(db, limit=0)


@app.post("/todo/", response_model=schemas.TodoReturn)
def add_todo(todo: schemas.TodoBase, db: Session = Depends(get_db)):
    """ A POST request for adding a todo
    
    Keyword Arguments:
    todo -- The todo to insert
    db -- The database session

    Returns the added todo if successful.
    """
    if last_todo := crud.get_last_todo(db):
        new_rank = str(parse(last_todo.rank).next())
    else:
        # BUCEKT_0 is an actual typo in the library
        new_rank = str(middle(Bucket.BUCEKT_0))

    new_todo = schemas.TodoCreate(
        description=todo.description,
        rank=new_rank
    )

    return crud.add_todo(db, todo=new_todo)


@app.put("/todo/", response_model=schemas.TodoReturn)
def update_todo(todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """ A PUT request to update an todo
    
    Keyword Arguments:
    todo -- The todo to update
    db -- The database session

    Returns the updated todo if successful.
    """
    return crud.update_todo_description(db, todo=todo)


@app.delete("/todo/", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """ A PUT request to delete an todo
    
    Keyword Arguments:
    todo_id -- The id of the todo to delete
    db -- The database session

    Deletes the todo
    """
    crud.delete_todo(db, todo_id=todo_id)


@app.put("/move_todo/", response_model=schemas.TodoReturn)
def move_todo(
    todo_id: int, 
    prev_todo_rank: Optional[str] = None,
    next_todo_rank: Optional[str] = None,
    db: Session = Depends(get_db)):
    """ A PUT request to move a todo, given its new neighboring todos
    
    Keyword Arguments:
    todo -- The todo to move
    prev_todo_rank -- the previous todo rank
    next_todo_rank -- the next todo rank
    db -- The database session

    Returns the moved todo if successful.
    """

    if prev_todo_rank and next_todo_rank:
        new_rank = str(between(parse(prev_todo_rank), parse(next_todo_rank)))
    elif prev_todo_rank:
        new_rank = str(parse(prev_todo_rank).next(step=LEXORANK_STEP))
    elif next_todo_rank:
        new_rank = str(parse(next_todo_rank).prev(step=LEXORANK_STEP))
    else:
        raise ValueError("Either add prev_todo_rank or next_todo_rank")
    
    return crud.update_todo_rank(db, todo_id=todo_id, new_rank=new_rank)


@app.put("/move_todo_to_pos/", response_model=schemas.TodoReturn)
def move_todo_to_pos(todo_id: int, new_pos: int, db: Session = Depends(get_db)):
    """ A PUT request to move a todo, given an index
    
    Keyword Arguments:
    todo -- The todo to move
    new_pos -- New position/index of todo
    db -- The database session

    Returns the moved todo if successful.
    """
    if new_pos == 0:
        first_todo = crud.get_first_todo(db)
        new_rank = str(parse(first_todo.rank).prev(LEXORANK_STEP))
    else:
        todos = crud.get_many_todos(db, limit=new_pos+1)
        if len(todos) == new_pos+1:
            new_rank = str(between(parse(todos[-2].rank), parse(todos[-1].rank)))
        else:
            new_rank = str(parse(todos[-1].rank).next(LEXORANK_STEP))

    return crud.update_todo_rank(db, todo_id=todo_id, new_rank=new_rank)

