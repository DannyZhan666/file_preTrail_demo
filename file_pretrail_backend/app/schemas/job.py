from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RawJobListForClientVO(BaseModel):
    jobId: int
    jobName: str
    jobType: str
    clientBudget: float
    issueDate: datetime

    class Config:
        orm_mode = True

class JobCreateRequest(BaseModel):
    job_name: str  # 工单名称
    job_type: int  # 工单类型
    job_intro: Optional[str] = None  # 工单简介
    client_budget: int  # 预期金额
    expected_time: Optional[datetime] = None  # 预期完成时间
    file_id: Optional[int] = None  # 文件 ID（如果有文件上传）

    class Config:
        orm_mode = True  # 支持 ORM 模型转换

class JobResponse(BaseModel):
    id: int
    job_name: str
    job_type: int
    job_intro: Optional[str] = None
    client_id: int
    client_budget: int
    due: Optional[datetime] = None
    file_id: Optional[int] = None
    create_time: datetime
    update_time: datetime
    is_deleted: int

    model_config = {
        "from_attributes": True
    }
