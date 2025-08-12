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
    job_id: int

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换
