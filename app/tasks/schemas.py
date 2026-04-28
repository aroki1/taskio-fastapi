from pydantic import BaseModel

class TaskTitle(BaseModel):
    title: str
