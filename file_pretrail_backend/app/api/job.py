from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.services.job_service import list_raw_job_for_client
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
