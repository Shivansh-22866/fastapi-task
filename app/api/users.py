from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, User
from app.database.mongodb import get_database
from app.auth.security import create_access_token
import bcrypt

router = APIRouter()

@router.post("/users", response_model=User)
async def create_user(user: UserCreate, db = Depends(get_database)):
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    result = await db.users.insert_one(user_dict)
    
    created_user = await db.users.find_one({"_id": result.inserted_id})
    return User(id=str(created_user["_id"]), email=created_user["email"], full_name=created_user["full_name"])

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_database)):
    user = await db.users.find_one({"email": form_data.username})
    if not user or not bcrypt.checkpw(form_data.password.encode(), user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token({"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}