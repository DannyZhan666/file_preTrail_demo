from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime



class MyOrder(BaseModel):
    id: Optional[int] = None
    order_name: Optional[str] = Field(default=None, alias="order_name")
    lawyer_id: Optional[int] = Field(default=None, alias="lawyer_id")
    client_id: Optional[int] = Field(default=None, alias="client_id")
    jid: Optional[int] = None
    create_time: Optional[datetime] = Field(default=None, alias="create_time")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }

class OrderCreateRequest(BaseModel):
    order_name: str
    new_jid: int
    origin_jid: int

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换

class OrderForLaywerVO(BaseModel):
    id: Optional[int] = None
    order_name: str
    client_name: Optional[str] = None
    create_time: datetime
    client_due_date: Optional[datetime] = None
    lawyer_due_date: Optional[datetime] = None

    class Config:
        orm_mode = True  # 使 Pydantic 支持 SQLAlchemy ORM 模型转换

class OrderForClientVO(BaseModel):
    id: Optional[int] = None
    order_name: str
    lawyer_name: Optional[str] = None
    create_time: datetime
    client_due_date: Optional[datetime] = None
    lawyer_due_date: Optional[datetime] = None

    class Config:
        orm_mode = True  # 使 Pydantic 支持 SQLAlchemy ORM 模型转换
