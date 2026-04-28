from fastapi import FastAPI

from app.exception_handlers import register_exception_handlers
from app.tasks.router import router as task_router

app = FastAPI()

app.include_router(router=task_router)
register_exception_handlers(app)