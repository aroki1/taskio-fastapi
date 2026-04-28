import uuid
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

class TaskStatus(StrEnum):
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

@dataclass
class Task:
    id: uuid.UUID
    title: str
    status: TaskStatus = TaskStatus.IN_PROGRESS
    
    def to_dict(self) -> dict[str, str]:
        return {
            "id": str(self.id),
            "title": self.title,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        return cls(
            id=uuid.UUID(data["id"]),
            title=data["title"],
            status=TaskStatus(data["status"])
        )
        
    def __repr__(self) -> str:
        repr_text = (
            f"ID: {self.id}\n"
            f"Title: {self.title}\n"
            f"Status: {self.status}"
        )
        return repr_text