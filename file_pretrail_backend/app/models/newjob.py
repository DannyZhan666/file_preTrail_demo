from sqlalchemy import Column, BigInteger, String, Integer, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.core.database import Base

class NewJob(Base):
    __tablename__ = 'newJob'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='工单id')
    job_id = Column(BigInteger, nullable=False, comment='原工单id')
    job_name = Column(String(256), nullable=False, comment='工单名')
    job_type = Column(Integer, nullable=False, comment='工单种类')
    job_intro = Column(String(1024), nullable=True, comment='工单简介')
    file_id = Column(BigInteger, nullable=False, comment='文件id')
    client_id = Column(BigInteger, nullable=False, comment='客户id')
    client_budget = Column(BigInteger, nullable=True, comment='客户预算')
    due = Column(DateTime, nullable=True, comment='逾期时间')
    lawyer_id = Column(BigInteger, nullable=True, comment='律师id')
    lawyer_budget = Column(BigInteger, nullable=True, comment='律师预算')
    lawyer_comment = Column(String(2048), nullable=True, comment='律师批注')
    due_law = Column(DateTime, nullable=True, comment='律师的预期时间')
    job_status = Column(SmallInteger, default=0, nullable=False, comment='工单状态')
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment='是否删除(0-未删, 1-已删)')
