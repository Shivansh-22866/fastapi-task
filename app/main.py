from fastapi import FastAPI
from app.api import users, tasks, analytics
from app.database.mongodb import get_database
from pymongo import ASCENDING

app = FastAPI(title="Task Management API")

# Register routers
app.include_router(users.router, tags=["users"])
app.include_router(tasks.router, tags=["tasks"])
app.include_router(analytics.router, tags=["analytics"])

@app.on_event("startup")
async def create_indexes():
    db = await anext(get_database())
    await db.users.create_index([("email", ASCENDING)], unique=True)
    await db.tasks.create_index([("assigned_to", ASCENDING), ("due_date", ASCENDING)])