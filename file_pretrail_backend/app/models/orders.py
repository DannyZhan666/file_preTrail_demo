from sqlalchemy import Column, BigInteger, String, DateTime, SmallInteger
from sqlalchemy.sql import func
from app.core.database import Base

class Orders(Base):
    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='订单id')
    order_name = Column(String(256), nullable=False, comment='订单名')
    client_id = Column(BigInteger, nullable=False, comment='客户id')
    lawyer_id = Column(BigInteger, nullable=False, comment='律师id')
    new_jid = Column(BigInteger, nullable=False, comment='新工单id')
    origin_jid = Column(BigInteger, nullable=False, comment='原工单id')
    create_time = Column(DateTime, nullable=False, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='更新时间')
    is_deleted = Column(SmallInteger, default=0, nullable=False, comment='是否删除(0-未删, 1-已删)')
