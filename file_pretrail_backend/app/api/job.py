import base64
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.models.file import MyFile
from app.models.job import Job
from app.models.user import User
from app.schemas.job import JobCreateRequest, JobResponse, JobDetailsForClientVO, NewJobCreateRequest, AcceptJobRequest
from app.services.file_service import file_analysis
from app.services.job_service import list_raw_job_for_client, list_new_job_for_client, \
    list_raw_job_for_lawyer, details_for_client, details, list_new_job_for_lawyer, details_for_accept, new_job, \
    accept_job, delete_origin_job_for_client, delete_new_job_for_client
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

@router.get("/list")
async def list_raw_job_for_lawyer_api(page: int, pageSize: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    获取律师未处理的工单列表，分页查询。
    """
    lawyer_id = current_user.id  # 当前用户是律师
    if not lawyer_id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用 service 层获取未处理的工单列表
        job_list = list_raw_job_for_lawyer(page, pageSize, lawyer_id, db)
        return ResultUtils.success(job_list)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/listNewJobForLawyer")
async def list_new_job_for_lawyer_api(page: int, pageSize: int, db: Session = Depends(get_db),
                                  current_user: User = Depends(get_current_user)):
    """
    获取律师的新工单列表，分页查询。
    """
    lawyer_id = current_user.id  # 获取当前用户ID
    if not lawyer_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 service 层获取分页后的新工单列表
    job_list = list_new_job_for_lawyer(page, pageSize, lawyer_id, db)
    return ResultUtils.success(job_list)

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

        # 调用文件分析函数
    file_analysis_result = file_analysis(job_create_request.file_id, db)

    # 如果文件分析失败，返回错误信息
    if file_analysis_result['status'] == "failure":
        raise HTTPException(status_code=400, detail=file_analysis_result['msg'])

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

@router.post("/newJob")
async def new_job_api(new_job_create_request: NewJobCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    创建一个新工单
    """
    user_id = current_user.id  # 获取当前用户ID
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 service 层创建新工单
    result = new_job(new_job_create_request, user_id, db)
    if result == 0:
        raise HTTPException(status_code=400, detail="工单不存在")

    return result

@router.post("/acceptJob")
async def accept_job_api(req: AcceptJobRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    接收一个工单，并创建对应的订单
    """
    user_id = current_user.id  # 获取当前用户ID
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 service 层接收工单
    result = accept_job(req.job_id, user_id, db)
    if result == -1:
        raise HTTPException(status_code=500, detail="接收工单失败")

    return result


@router.get("/details")
async def get_job_details(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    获取工单详情接口
    """
    user_id = current_user.id  # 获取当前用户ID
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 service 层获取工单详情
    job_details = details(id, user_id, db)
    if not job_details:
        raise HTTPException(status_code=404, detail="工单未找到")

    return ResultUtils.success(job_details)

@router.get("/detailsForClient")
async def details_for_client_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    获取工单详情接口，用户登录后才能查看工单。
    """
    # 用户验证
    if not current_user.id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用 service 层获取工单详情
        job_details = details_for_client(id, db, current_user.id)
        return ResultUtils.success(job_details)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/detailsForAccept")
async def get_job_details_for_accept(id: int, db: Session = Depends(get_db),
                                     current_user: User = Depends(get_current_user)):
    """
    获取工单的详细信息以供接收
    """
    user_id = current_user.id  # 获取当前用户ID
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 service 层获取工单详细信息
    job_details = details_for_accept(id, user_id, db)
    if not job_details:
        raise HTTPException(status_code=404, detail="工单未找到")

    return ResultUtils.success(job_details)

@router.delete("/deleteOriginJobForClient")
async def delete_origin_job_for_client_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    根据ID删除工单
    """
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 job_service 中的删除方法
    result = delete_origin_job_for_client(id, user_id, db)
    return ResultUtils.success(result)

@router.delete("/deleteNewJobForClient")
async def delete_new_job_for_client_api(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    根据ID删除工单
    """
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用 job_service 中的删除方法
    result = delete_new_job_for_client(id, user_id, db)
    return ResultUtils.success(result)