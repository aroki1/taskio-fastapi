# taskio-fastapi

A simple task tracker API written in Python with FastAPI.

## Features

- Add tasks
- List tasks
- Get a task by id
- Update tasks
- Complete tasks
- Delete tasks
- Save tasks to JSON
- Load tasks from JSON

## Requirements

- Python 3.12+
- uv - An extremely fast Python package and project manager, written in Rust.

## Quick start

```bash
git clone https://github.com/aroki1/taskio-fastapi.git
cd taskio-fastapi
uv run fastapi dev app/main.py
```

To open docs:

```text
http://127.0.0.1:8000/docs
```

## Storage

By default, tasks are stored in memory.

To use JSON storage:

```bash
TASK_REPOSITORY=json TASKS_PATH=tasks.json uv run fastapi dev app/main.py
```

## Project structure

```text
.
├── app
│   ├── __init__.py
│   ├── main.py
│   └── tasks
│       ├── errors.py
│       ├── __init__.py
│       ├── models.py
│       ├── repository.py
│       ├── schemas.py
│       └── service.py
├── pyproject.toml
└── README.md
```
