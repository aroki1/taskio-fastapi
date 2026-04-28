import uuid


class TaskError(Exception):
    pass

class TaskNotFoundError(TaskError):
    def __init__(self, task_id: uuid.UUID, message ="Task not found, id: {task_id}") -> None:
        self.message = message.format(task_id=task_id)
        super().__init__(self.message)

class TaskEmptyTitleError(TaskError):
    def __init__(self, message = "Task title cannot be empty") -> None:
        self.message = message
        super().__init__(self.message)

class TaskAlreadyExistsError(TaskError):
    def __init__(self, message = "Task already exists") -> None:
        self.message = message
        super().__init__(self.message)