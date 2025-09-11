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

class JobListForLawyerVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    client_name: Optional[str] = None
    client_budget: int
    issue_date: datetime

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换

class NewJobListForLawyerVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    job_intro: Optional[str] = None
    client_name: Optional[str] = None
    client_budget: int
    issue_date: datetime
    update_time: datetime

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换


class JobCreateRequest(BaseModel):
    job_name: str  # 工单名称
    job_type: int  # 工单类型
    job_intro: Optional[str] = None  # 工单简介
    client_budget: int  # 预期金额
    expected_time: Optional[datetime] = None  # 预期完成时间
    file_id: Optional[int] = None  # 文件 ID（如果有文件上传）

    class Config:
        orm_mode = True  # 支持 ORM 模型转换

class NewJobCreateRequest(BaseModel):
    job_id: int
    lawyer_budget: int
    lawyer_comment: Optional[str]
    lawyer_expected_time: Optional[datetime]

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换

class AcceptJobRequest(BaseModel):
    job_id: int

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


class JobDetailsVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    job_intro: str
    client_id: int
    client_name: Optional[str] = None
    client_budget: int
    expected_time: datetime
    issue_date: datetime
    file_content: Optional[str] = None
    path: Optional[str] = None
    file_name: Optional[str] = None
    page_num: Optional[int] = None
    paragraph: Optional[str] = None
    paragraph_clean: Optional[str] = None
    model_predict_details: Optional[str] = None
    model_predict_labels: Optional[str] = None

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换

class JobDetailsForClientVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    job_intro: Optional[str]
    client_id: int
    client_name: Optional[str] = None
    client_budget: int
    due: Optional[datetime]
    issue_date: datetime
    file_content: Optional[str] = None
    path: Optional[str] = None
    file_name: Optional[str] = None
    lawyer_id: int
    lawyer_name: Optional[str] = None
    lawyer_budget: int
    lawyer_comment: Optional[str]
    update_time: datetime
    due_law: Optional[datetime]
    page_num: Optional[int] = None
    paragraph: Optional[str] = None
    paragraph_clean: Optional[str] = None
    model_predict_details: Optional[str] = None
    model_predict_labels: Optional[str] = None

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换

class JobDetailsForAcceptVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    job_intro: str
    client_id: int
    client_account: Optional[str] = None
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    client_email: Optional[str] = None
    client_budget: int
    issue_date: datetime
    file_content: Optional[str] = None
    path: Optional[str] = None
    file_name: Optional[str] = None
    page_num: Optional[int] = None
    paragraph: Optional[str] = None
    paragraph_clean: Optional[str] = None
    model_predict_details: Optional[str] = None
    model_predict_labels: Optional[str] = None

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换