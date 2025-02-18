from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.models.task import TaskCreate, Task, TaskUpdate
from app.models.user import User
from app.database.mongodb import get_database
from app.auth.security import get_current_user
from datetime import datetime
from bson import ObjectId
from pymongo import ASCENDING

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db = Depends(get_database)):
    task_dict = task.dict()
    task_dict["created_at"] = datetime.utcnow()
    task_dict["status"] = "pending"
    task_dict["assigned_to"] = current_user.id
    
    result = await db.tasks.insert_one(task_dict)
    created_task = await db.tasks.find_one({"_id": result.inserted_id})
    return Task(id=str(created_task["_id"]), **created_task)

@router.get("/tasks", response_model=List[Task])
async def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    query = {"assigned_to": current_user.id}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    
    cursor = db.tasks.find(query).sort("due_date", ASCENDING)
    tasks = await cursor.to_list(length=None)
    return [Task(id=str(task["_id"]), **task) for task in tasks]

@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str, current_user: User = Depends(get_current_user), db = Depends(get_database)):
    task = await db.tasks.find_one({"_id": ObjectId(task_id), "assigned_to": current_user.id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Task(id=str(task["_id"]), **task)

@router.patch("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db = Depends(get_database)
):
    task = await db.tasks.find_one({"_id": ObjectId(task_id), "assigned_to": current_user.id})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    if update_data:
        await db.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
    
    updated_task = await db.tasks.find_one({"_id": ObjectId(task_id)})
    return Task(id=str(updated_task["_id"]), **updated_task)

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, current_user: User = Depends(get_current_user), db = Depends(get_database)):
    result = await db.tasks.delete_one({"_id": ObjectId(task_id), "assigned_to": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}