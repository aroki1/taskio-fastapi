# API
import uuid

from app.tasks.errors import TaskAlreadyExistsError, TaskEmptyTitleError, TaskNotFoundError
from app.tasks.models import Task, TaskStatus
from app.tasks.repository import TaskRepository

class TaskService():
    def __init__(self, repository: TaskRepository) -> None:
        self.tasks = repository.load_tasks()
        self.repository = repository

    def get_task(self, task_id: uuid.UUID):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def add_task(self, task_title: str) -> Task:
        normalized_title = task_title.strip()
        if normalized_title == "":
            raise TaskEmptyTitleError()
        
        if any(task.title == normalized_title for task in self.tasks):
            raise TaskAlreadyExistsError()

        task = Task(uuid.uuid4(), normalized_title, TaskStatus.IN_PROGRESS)
        self.tasks.append(task)
        self.repository.save_tasks(self.tasks)
        
        return task
    
    def list_tasks(self) -> list[Task]:
        return self.tasks

    def complete_task(self, task_id: uuid.UUID) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                self.repository.save_tasks(self.tasks)
                return task
            
        raise TaskNotFoundError(task_id)

    def update_task(self, task_new: Task) -> Task:
        normalized_title = task_new.title.strip()
        if normalized_title == "":
            raise TaskEmptyTitleError()

        if any(task.id != task_new.id and task.title == normalized_title for task in self.tasks):
            raise TaskAlreadyExistsError()

        for task in self.tasks:
            if task.id == task_new.id:
                task.title = normalized_title
                task.status = task_new.status
                self.repository.save_tasks(self.tasks)
                return task

        raise TaskNotFoundError(task_new.id)

    def update_task_title(self, task_id: uuid.UUID, task_title: str) -> Task:
        normalized_title = task_title.strip()
        if normalized_title == "":
            raise TaskEmptyTitleError()
        
        if any(task.id != task_id and task.title == normalized_title for task in self.tasks):
            raise TaskAlreadyExistsError()
        
        for task in self.tasks:
            if task.id == task_id:
                task.title = normalized_title
                self.repository.save_tasks(self.tasks)
                return task
                
        raise TaskNotFoundError(task_id)
        
    def delete_task(self, task_id: uuid.UUID) -> Task:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                task = self.tasks.pop(i)
                self.repository.save_tasks(self.tasks)
                return task
            
        raise TaskNotFoundError(task_id)