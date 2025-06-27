from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar('T')  # 泛型类型

class BaseResponse(BaseModel, Generic[T]):
    code: int
    data: Optional[T] = None
    msg: str
    description: Optional[str] = None

    class Config:
        # 使用 jsonable_encoder，避免某些复杂类型导致的错误
        json_encoders = {
            dict: lambda v: str(v),  # 对字典类型进行编码
        }
