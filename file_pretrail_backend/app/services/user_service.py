import os
import shutil
import uuid

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegister
from app.utils.page_help import paginate

AVATAR_DIRECTORY = "avatar"  # 文件保存路径

def create_user(db: Session, user: UserRegister):
    db_user = User(
        user_account=user.user_account,
        user_password=user.user_password,
        username=user.username,
        email=user.email,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_lawyers(db: Session, user_id: int, page: int, page_size: int):
    # Get the user role from the db if necessary
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None  # or raise an exception

    # Query for lawyers
    query = db.query(User).filter(User.user_role == 2, User.is_deleted == 0)
    return paginate(query, page, page_size)

def upload_avatar(file: UploadFile, user_id: int, db: Session):
    """
    处理用户头像上传，保存文件并更新数据库中的 avatarUrl 字段
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    try:
        # 读取文件内容并保存到变量，确保文件不会被消费
        file_content = file.read()  # 读取文件内容

        # 获取文件扩展名
        file_extension = file.filename.split('.')[-1].lower()

        # 生成新的文件名，避免文件名冲突
        file_name = str(uuid.uuid4()) + '.' + file_extension

        file_path = os.path.join(AVATAR_DIRECTORY, file_name)

        if not os.path.exists(AVATAR_DIRECTORY):
            os.makedirs(AVATAR_DIRECTORY)
        with open(file_path, "wb") as f:
            f.write(file.file.read())  # 使用 file.file.read() 而非 file.read()


        # 更新用户的头像 URL
        user.avatar_url = str(file_path)  # 存储文件路径
        db.commit()

        # 刷新用户对象，确保获取最新的用户数据
        db.refresh(user)

        return user.avatar_url  # 返回新的头像路径

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"头像上传失败: {str(e)}")