from sqlalchemy import Column, Integer, BigInteger, String, DateTime, SmallInteger, func
from app.core.database import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "file_task"}  # 指定 schema（数据库名）

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    username = Column(String(256), nullable=True, comment="用户昵称")
    user_account = Column(String(256), nullable=True, comment="账号")
    user_password = Column(String(512), nullable=False, comment="密码")
    gender = Column(SmallInteger, nullable=True, comment="性别")
    avatar_url = Column(String(1024), nullable=True, comment="用户头像")
    phone = Column(String(128), nullable=True, comment="手机号")
    email = Column(String(512), nullable=True, comment="邮箱")
    user_status = Column(Integer, nullable=False, default=0, comment="状态")
    user_role = Column(Integer, nullable=False, default=1, comment="用户角色 0-管理员 1-律师 2-客户")
    create_time = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="是否删除(0-未删, 1-已删)")
