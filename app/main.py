
import os
import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.tasks.errors import TaskAlreadyExistsError, TaskNotFoundError, TaskEmptyTitleError
from app.tasks.schemas import TaskTitle
from app.tasks.repository import InMemoryRepository, JsonTaskRepository, TaskRepository
from app.tasks.service import TaskService
from app.tasks.models import Task

def create_task_repository() -> TaskRepository:
    repo = os.getenv("TASK_REPOSITORY", "in-memory")
    
    if repo == "in-memory":
        return InMemoryRepository()
    elif repo == "json":
        path = os.getenv("TASKS_PATH", "tasks.json")
        return JsonTaskRepository(path)
    
    raise ValueError(f"Unknown repository: {repo}")

repository = create_task_repository()
task_service_instance = TaskService(repository)

def get_task_service() -> TaskService:
    return task_service_instance

app = FastAPI()
TaskServiceDepends = Annotated[TaskService, Depends(get_task_service)]

@app.exception_handler(TaskAlreadyExistsError)
async def task_already_exists_handler(request: Request, exc: TaskAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"error": "Task already exists", "message": "Task with this title already exists"},
    )

@app.exception_handler(TaskNotFoundError)
async def task_not_found_error_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": "Task does not exist", "message": "Task with this id does not exist"},
    )

@app.exception_handler(TaskEmptyTitleError)
async def task_empty_title_error_handler(request: Request, exc: TaskEmptyTitleError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Task title cannot be empty", "message": "Task title cannot be empty"},
    )

@app.get("/tasks")
async def get_tasks(service: TaskServiceDepends):
    return service.list_tasks()

@app.get("/tasks/{task_id}")
async def get_task(service: TaskServiceDepends, task_id: uuid.UUID) -> Task:
    return service.get_task(task_id)

@app.post("/tasks")
async def add_task(task_title: TaskTitle, service: TaskServiceDepends) -> Task:
    return service.add_task(str(task_title.title))

@app.patch("/tasks")
async def update_task(task: Task, service: TaskServiceDepends) -> Task:
    return service.update_task(task)

@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: uuid.UUID, service: TaskServiceDepends):
    return service.complete_task(task_id)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: uuid.UUID, service: TaskServiceDepends):
    return service.delete_task(task_id)