import os
from app.tasks.repository import TaskRepository, InMemoryRepository, JsonTaskRepository
from app.tasks.service import TaskService


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
