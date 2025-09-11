from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class NewJobListForClientVO(BaseModel):
    job_id: int
    job_name: str
    job_type: int
    client_budget: int
    due: Optional[datetime]
    lawyer_name: Optional[str] = None
    lawyer_budget: Optional[int] = None
    due_law: Optional[datetime] = None
    issue_date: datetime
    update_date: Optional[datetime] = None

    class Config:
        orm_mode = True  # 允许从 ORM 对象转换


class NewJobDetailsForClientVO(BaseModel):
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

class NewJobDetailsForAcceptVO(BaseModel):
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