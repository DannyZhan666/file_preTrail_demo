import base64
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.models.file import MyFile
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreateRequest, JobResponse, JobDetailsForClientVO
from app.services.job_service import list_raw_job_for_client, get_job_details, list_new_job_for_client
from app.core.database import get_db
from app.utils.result_utils import ResultUtils

router = APIRouter()

@router.get("/listForClient")
def list_raw_job_for_client_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    获取用户的工单列表，通过 JWT Token 提取用户信息。
    """
    try:
        # 使用从 JWT 中获取的 current_user（即用户的 user_id）
        client_id = current_user.id
        result = list_raw_job_for_client(db, page, pageSize, client_id)
        return ResultUtils.success(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.get("/listNewJobForClient")
async def list_new_job_for_client_api(page: int = 1, pageSize: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    获取新的工单列表接口，区分客户端和律师。
    """
    user_id = current_user.id  # 当前用户 ID
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用 service 层获取新的工单列表
        job_list = list_new_job_for_client(page, pageSize, user_id, db)
        return ResultUtils.success(job_list)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/create")
async def create_job(
    job_create_request: JobCreateRequest,  # 从前端接收的工单数据
    db: Session = Depends(get_db),  # 数据库会话
    current_user: User = Depends(get_current_user)  # 获取当前登录的用户
):
    """
    创建工单接口，用户登录后才能创建工单。
    """
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 校验工单名称和类型
    if not job_create_request.job_name or not job_create_request.job_type:
        raise HTTPException(status_code=400, detail="工单名称和类型不能为空")

    # 创建工单对象
    new_job = Job(
        job_name=job_create_request.job_name,
        job_type=job_create_request.job_type,
        job_intro=job_create_request.job_intro,
        client_id=user_id,  # 使用当前用户的 ID
        client_budget=job_create_request.client_budget,
        due=job_create_request.expected_time,
        file_id=job_create_request.file_id,  # 文件 ID 可选
        create_time=datetime.now(),
        update_time=datetime.now(),
        is_deleted=0  # 工单未删除
    )

    # 保存到数据库
    db.add(new_job)
    db.commit()
    db.refresh(new_job)  # 获取新创建的工单对象

    # return ResultUtils.success({"data": {"jobId": new_job.id}})
    return ResultUtils.success({"data": JobResponse.from_orm(new_job)})  # 返回创建的工单对象（或根据需求返回工单 ID）

@router.get("/detailsForClient")
async def details_for_client(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    获取工单详情接口，用户登录后才能查看工单。
    """
    # 用户验证
    if not current_user.id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用 service 层获取工单详情
        job_details = get_job_details(id, db, current_user.id)
        return ResultUtils.success(job_details)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

