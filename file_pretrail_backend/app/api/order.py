from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_db, get_current_user
from app.models.user import User
from app.services.order_service import get_order_list
from app.utils.result_utils import ResultUtils

router = APIRouter()

@router.get("/list")
def list_orders(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id
    # 查询数据库获取 user_role
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user_role = db_user.user_role

    page_data = get_order_list(db, page, pageSize, user_id, user_role)

    return ResultUtils.success(page_data)
