from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: str
    tags: List[str] = []

class Task(TaskCreate):
    id: str
    created_at: datetime
    status: str
    assigned_to: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[List[str]] = None