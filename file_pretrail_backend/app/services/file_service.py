import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import uuid

from app.models.file import MyFile
from app.utils.alioss_utils import upload_to_oss

UPLOAD_DIRECTORY = "uploads"  # 文件保存路径
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB 文件大小限制


async def upload_file_service(file: UploadFile, user_id: int, db: Session):
    # 文件校验
    if not file:
        raise HTTPException(status_code=400, detail="文件为空，请重新上传")

    # 获取文件扩展名
    file_extension = file.filename.split('.')[-1].lower()
    # 读取文件内容并保存到变量，确保文件不会被消费
    file_content = await file.read()  # 读取文件内容
    # 获取文件大小
    file_size = len(file_content)

    # 校验文件大小（最大100MB）
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制，最大支持100MB")

    # 生成新的文件名，避免文件名冲突
    file_name = str(uuid.uuid4()) + '.' + file_extension

    # 上传文件到阿里云 OSS（你可以修改为保存到本地或者其他地方）
    file_path = upload_to_oss(file, file_name)  # 你可以修改这里来实现不同的存储方案

    # 将文件信息保存到数据库
    new_file = MyFile(
        file_name=file.filename,
        file_type=file_extension,
        path=file_path,  # 保存的路径
        content=file_content,  # 这里会保存文件内容
        create_time=datetime.now(),
        update_time=datetime.now(),
        is_deleted=0  # 文件未删除
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # 返回文件的ID
    return new_file.id
