from sqlalchemy import Column, BigInteger, String, Integer, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.core.database import Base

class Bids(Base):
    __tablename__ = 'bids'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='投标id')
    jid = Column(BigInteger, nullable=False, comment='工单id')
    lawyer_id = Column(BigInteger, nullable=True, comment='律师id')
    lawyer_budget = Column(BigInteger, nullable=True, comment='律师预算')
    lawyer_comment = Column(String(2048), nullable=True, comment='律师批注')
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment='是否删除(0-未删, 1-已删)')
