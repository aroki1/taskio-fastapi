import uuid
from pydantic import BaseModel
from app.tasks.models import TaskStatus

class TaskTitle(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str | None = None
    status: TaskStatus | None = None

class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    status: TaskStatus