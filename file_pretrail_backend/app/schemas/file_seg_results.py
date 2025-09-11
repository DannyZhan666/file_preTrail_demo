from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class FileSegResultsBase(BaseModel):
    fid: int
    paragraph: Optional[str]
    page_num: Optional[int]
    paragraph_clean: Optional[str]
    model_predict_details: Optional[Any]
    model_predict_labels: Optional[Any]


class FileSegResultsCreate(FileSegResultsBase):
    pass


class FileSegResults(FileSegResultsBase):
    id: int
    create_time: datetime
    update_time: datetime
    is_deleted: int

    class Config:
        orm_mode = True
