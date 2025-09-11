import os
import re
from io import BytesIO

import pymupdf
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import uuid

from sqlalchemy.testing import db

from app.models.file import MyFile
from app.models.file_seg_results import FileSegResults
from app.utils.alioss_utils import upload_to_oss
from app.utils.file_analysis_utils import get_special_condition_starting_page_index_new, get_all_text, load_kept_word, \
    ALL_PATTERN, load_model, select_kept_word, get_pred_result, SELECT_COLS

UPLOAD_DIRECTORY = "contracts"  # 文件保存路径
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1GB 文件大小限制


async def upload_file_service(file: UploadFile, user_id: int, db: Session):
    # 文件校验
    if not file:
        raise HTTPException(status_code=400, detail="文件为空，请重新上传")

    # check file type, pdf only for now
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="只能上传 PDF 文件")

    # 读取文件内容并保存到变量，确保文件不会被消费
    file_content = await file.read()  # 读取文件内容

    # 获取文件大小
    file_size = len(file_content)

    # 校验文件大小（最大100MB）
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小超过限制，最大支持100MB")

    # 获取文件扩展名
    file_extension = file.filename.split('.')[-1].lower()

    # 生成新的文件名，避免文件名冲突
    file_name = str(uuid.uuid4()) + '.' + file_extension

    # 上传文件到阿里云 OSS（你可以修改为保存到本地或者其他地方）
    file_path_alioss = upload_to_oss(file, file_name)  # 你可以修改这里来实现不同的存储方案
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)

    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    with open(file_path, "wb") as f:
        f.write(file_content)

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

def file_analysis(file_id: int, db: Session):
    """
    分析上传的文件，提取文本并进行清理和预测。
    """

    # 获取文件信息
    file = db.query(MyFile).filter(MyFile.id == file_id).first()
    if not file:
        return {"msg": "文件不存在", "status": "failure"}

    file_path = file.path
    file_content = file.content

    # check the file content
    try:
        doc = pymupdf.open(stream=file_content, filetype="pdf")
    except Exception:
        raise HTTPException(status_code=400, detail="文件内容无法解析为 PDF")

    # analysis contract
    # text = "\n".join([page.get_text() for page in doc])
    with pymupdf.open(stream=file_content, filetype="pdf") as doc:
        try:
            start_page = get_special_condition_starting_page_index_new(file_path)
        except Exception:
            raise Exception("Sorry, we can't find any special condition or maybe this is a scanned pdf")

        cur_pdf = get_all_text(file_path, doc, start_page)
        print(cur_pdf)
        all_kept_kw = load_kept_word()
        cur_pdf['paragraph'] = cur_pdf['paragraph'].apply(
            lambda x: ' '.join([i.lower().strip() for i in re.sub(ALL_PATTERN, ' ', x).lower().split(" ")]))
        cur_pdf['paragraph_clean'] = cur_pdf['paragraph'].apply(lambda x: select_kept_word(x, all_kept_kw))
        model = load_model()
        cur_pdf['model_predict_details'] = cur_pdf['paragraph_clean'].apply(lambda x: model.predict(x))
        cur_pdf['model_predict_labels'] = cur_pdf['model_predict_details'].apply(lambda x: get_pred_result(x))

    # 再保存段落信息
    for _, row in cur_pdf.iterrows():
        new_paragraph = FileSegResults(
            fid=file_id,
            paragraph=row['paragraph'],
            page_num=row['page_num'],
            paragraph_clean=row['paragraph_clean'],
            model_predict_details=str(row['model_predict_details']),
            model_predict_labels=str(row['model_predict_labels']),
            create_time=datetime.now(),
            update_time=datetime.now(),
            is_deleted=0  # 文件未删除
        )
        db.add(new_paragraph)
    db.commit()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        return {"msg": str(e), "status": "failure"}

    return {"msg": "文件分析并保存成功", "status": "success"}