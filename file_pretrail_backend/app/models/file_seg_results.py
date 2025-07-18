from sqlalchemy import Column, BigInteger, Text, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.core.database import Base

class FileSegResults(Base):
    __tablename__ = 'file_seg_results'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='段落id')
    fid = Column(BigInteger, nullable=False, comment='文件id')
    segment = Column(Text, nullable=True, comment='段落内容')
    prediction = Column(Text, nullable=True, comment='预测结果')
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment='是否删除(0-未删, 1-已删)')
