from fastapi import APIRouter, Depends
from app.models.user import User
from app.database.mongodb import get_database
from app.auth.security import get_current_user

router = APIRouter()

@router.get("/analytics/task-status")
async def get_task_status_analytics(current_user: User = Depends(get_current_user), db = Depends(get_database)):
    pipeline = [
        {"$match": {"assigned_to": current_user.id}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    result = await db.tasks.aggregate(pipeline).to_list(length=None)
    return {item["_id"]: item["count"] for item in result}

@router.get("/analytics/priority-distribution")
async def get_priority_analytics(current_user: User = Depends(get_current_user), db = Depends(get_database)):
    pipeline = [
        {"$match": {"assigned_to": current_user.id}},
        {"$group": {"_id": "$priority", "count": {"$sum": 1}}}
    ]
    result = await db.tasks.aggregate(pipeline).to_list(length=None)
    return {item["_id"]: item["count"] for item in result}