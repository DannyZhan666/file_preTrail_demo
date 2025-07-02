from pydantic import BaseModel, Field
from datetime import datetime



class MyOrder(BaseModel):
    id: int
    orderName: str = Field(alias="order_name")
    lawyerId: int = Field(alias="lawyer_id")
    clientId: int = Field(alias="client_id")
    jid: int
    createTime: datetime = Field(alias="create_time")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
