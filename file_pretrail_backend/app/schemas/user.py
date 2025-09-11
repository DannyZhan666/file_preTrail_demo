from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from typing import Optional


class UserRegister(BaseModel):
    user_account: str = Field(..., min_length=2)
    user_password: str = Field(..., min_length=8)
    check_password: str = Field(..., min_length=8)
    user_role: int = Field(..., ge=0, le=2)


class UserLogin(BaseModel):
    userAccount: str = Field(..., example="ckc", min_length=2)
    userPassword: str = Field(..., example="12345678", min_length=6)

    class Config:
        schema_extra = {
            "example": {
                "userAccount": "test_user",
                "userPassword": "password123"
            }
        }

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    id: int
    username: str
    user_account: str
    gender: Optional[int] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    user_role: UserRole
    create_time: datetime

    class Config:
        orm_mode = True  # 如果使用 SQLAlchemy ORM

class LawyerResponse(BaseModel):
    id: int
    username: Optional[str] = ''  # 设置默认值为空字符串
    gender: Optional[int] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    create_time: datetime  # 使用前端传递的格式化时间

    class Config:
        orm_mode = True  # 允许Pydantic从ORM对象中提取数据

class UpdateUserRequest(BaseModel):
    username: str
    gender: Optional[int] = None  # 性别为可选字段，默认为 None
    avatarUrl: Optional[str] = None  # 头像为可选字段，默认为 None
    phone: str
    email: str

    class Config:
        orm_mode = True  # 允许从 SQLAlchemy 模型转换到 Pydantic 模型
