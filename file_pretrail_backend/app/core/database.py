import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # 加载项目根目录下的 .env 文件

DATABASE_URL = os.getenv("DB_URL")

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True)

# 创建本地 session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 基类
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

