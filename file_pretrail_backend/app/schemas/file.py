from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MyFileBase(BaseModel):
    file_name: str  # 文件名
    file_type: str  # 文件类型
    path: str  # 文件路径
    content: str  # 文件内容（这里可以选择为字符串，便于传输文件的 Base64 编码）

    class Config:
        orm_mode = True  # 允许从数据库模型转换为 Pydantic 模型

class MyFileCreate(MyFileBase):
    # 创建文件时需要的字段
    pass

class MyFileResponse(MyFileBase):
    id: int  # 文件 ID
    create_time: datetime  # 创建时间
    update_time: datetime  # 更新时间
    is_deleted: int  # 是否删除

    class Config:
        orm_mode = True  # 允许从数据库模型转换为 Pydantic 模型
