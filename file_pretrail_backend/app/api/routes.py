import re

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.api import user, job, order, file
from app.core.auth import get_password_hash, verify_password, create_access_token
from app.core.database import SessionLocal, get_db
from app.models.user import User
from app.schemas.item import Item
from app.schemas.user import UserRegister, UserLogin
from app.services.item_service import process_item

router = APIRouter()
router.include_router(user.router)
# 注册 job 路由
router.include_router(job.router, prefix="/job", tags=["job"])
router.include_router(order.router, prefix="/order", tags=["order"])
router.include_router(file.router, prefix="/file", tags=["file"])


@router.get("/hello")
def say_hello():
    return {"message": "Hello from FastAPI!"}


@router.post("/items/")
def create_item(item: Item):
    result = process_item(item)
    return {"result": result}


