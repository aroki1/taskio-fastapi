from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.tasks.errors import TaskAlreadyExistsError, TaskEmptyTitleError, TaskError,TaskNotFoundError

TASK_ERROR_RESPONSES = {
    TaskAlreadyExistsError: (
        status.HTTP_409_CONFLICT,
        "Task already exists",
        "Task with this title already exists",
    ),
    TaskNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "Task does not exist",
        "Task with this id does not exist",
    ),
    TaskEmptyTitleError: (
        status.HTTP_400_BAD_REQUEST,
        "Task title cannot be empty",
        "Task title cannot be empty",
    ),
}


async def task_error_handler(request: Request, exc: TaskError):
    status_code, error, message = TASK_ERROR_RESPONSES[type(exc)]

    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "message": message,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(TaskError, task_error_handler)