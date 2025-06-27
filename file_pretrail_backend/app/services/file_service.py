import os
from fastapi import HTTPException
from app.models.file import File
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import uuid

UPLOAD_DIRECTORY = "uploads"  # 文件保存路径
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB 文件大小限制


async def upload_file_service(file, user_id: int, db: Session):
    # 文件校验
    if not file:
        raise HTTPException(status_code=400, detail="文件为空，请重新上传")

    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制，最大支持 1GB")

    # 获取文件的原始名称和扩展名
    original_filename = file.filename
    file_extension = original_filename.split('.')[-1].lower()

    # 生成新的文件名（使用 UUID 避免文件名冲突）
    object_name = str(uuid.uuid4()) + '.' + file_extension

    # 保存文件到指定路径
    file_path = os.path.join(UPLOAD_DIRECTORY, object_name)
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)

    try:
        # 保存文件到本地
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

    # 将文件信息保存到数据库
    new_file = File(
        file_name=original_filename,
        file_type=file_extension,
        path=file_path,
        content=file.file.read(),  # 存储文件内容的字节流
        create_time=datetime.utcnow(),
        update_time=datetime.utcnow(),
        is_deleted=0
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # 返回文件的ID
    return new_file.id
