import uuid
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from app.dependencies import get_task_service
from app.tasks.service import TaskService
from app.tasks.schemas import TaskRead, TaskUpdate, TaskTitle

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskServiceDepends = Annotated[TaskService, Depends(get_task_service)]

@router.get("", response_model=list[TaskRead])
async def get_tasks(service: TaskServiceDepends):
    return service.list_tasks()

@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task_id: uuid.UUID, service: TaskServiceDepends):
    return service.get_task(task_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def add_task(task_title: TaskTitle, service: TaskServiceDepends):
    return service.add_task(str(task_title.title))

@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(task_id: uuid.UUID, task: TaskUpdate, service: TaskServiceDepends) :
    return service.update_task(task_id, task.title, task.status)

@router.patch("/{task_id}/complete", response_model=TaskRead)
async def complete_task(task_id: uuid.UUID, service: TaskServiceDepends):
    return service.complete_task(task_id)

@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(task_id: uuid.UUID, service: TaskServiceDepends):
    return service.delete_task(task_id)