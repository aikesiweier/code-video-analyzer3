from pydantic import BaseModel, Field
from datetime import datetime

class TaskCreateResponse(BaseModel):
    task_id: int
    status: str

class TaskStatusResponse(BaseModel):
    task_id: int = Field(..., validation_alias='id', serialization_alias='task_id')
    status: str
    progress: int
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True