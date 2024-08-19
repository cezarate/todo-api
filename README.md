# todo-api

This is a simple API for a todo list that implements Lexorank (lexicographical sorting)
## Features

The SQLite database this API connects to has one table named "todos" which has the following columns: 

    - todo_id: int
    - description: str
    - rank: str

This API has the following routes:

    - [GET] /todo/
        - returns all items from the todo list, sorted
    - [POST] /todo/
        - adds an todo item
    - [PUT] /todo/
        - updates a todo item
    - [DELETE] /todo/{todo_id}
        - deletes a todo item
    - [PUT] /move_todo/
        - move todo item between two todo items provided the todo item and the adjacent todo ranks
    - [PUT] /move_todo_by_pos/
        - move todo item by index
## Environment Variables

To run this project, add the following to the .env file

    DB_NAME="todos_db"

## Run Locally

Clone the project:

```bash
  git clone https://github.com/cezarate/todo-api.git
```

Go to the project directory:

```bash
  cd TODO-API
```

Install dependencies:

```bash
  poetry shell
  poetry install
```

Run:
```bash
  uvicorn todo.main:app --reload
```

## Testing
Once the API has started, go to localhost:8000/docs to access the interactive API


## 🚀 About Me
I'm a software developer.

