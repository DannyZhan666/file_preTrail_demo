from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger, Text, LargeBinary
from sqlalchemy.sql import func
from app.core.database import Base


class MyFile(Base):
    __tablename__ = 'file'

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment='文件id')
    file_name = Column(String(256), nullable=False, comment='文件名')
    file_type = Column(String(50), nullable=False, comment='文件类型')
    path = Column(String(1024), nullable=False, comment='文件路径')
    content = Column(LargeBinary, nullable=False, comment='文件内容') # 文件内容（二进制数据）
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment='是否删除(0-未删, 1-已删)')
