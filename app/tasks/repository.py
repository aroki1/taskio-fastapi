import json
from typing import Protocol

from app.tasks.models import Task

class TaskRepository(Protocol):
    def __init__(self) -> None:
        pass
    
    def save_tasks(self, tasks: list[Task]) -> None:
        ...
    
    def load_tasks(self) -> list[Task]:
        ...

class JsonTaskRepository(TaskRepository):
    def __init__(self, path: str) -> None:
        self.path = path
            
    def save_tasks(self, tasks: list[Task]) -> None:
        with open(self.path, 'w') as f:
            json_str = json.dumps([task.to_dict() for task in tasks], indent=4)
            f.write(json_str)
        
    def load_tasks(self) -> list[Task]:
        try:
            with open(self.path, 'r') as f:
                tasks = json.loads(f.read())
                return [Task.from_dict(task) for task in tasks]
        except FileNotFoundError:
            return []
        
class InMemoryRepository(TaskRepository):
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self.tasks = tasks if tasks is not None else []
    
    def save_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks
    
    def load_tasks(self) -> list[Task]:
        return self.tasks