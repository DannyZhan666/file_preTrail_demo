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
