from sqlalchemy.orm import Session
from typing import Dict, List
from fastapi import HTTPException

from app.models.orders import Orders
from app.schemas.order import MyOrder


def get_order_list(
    db: Session,
    page: int,
    page_size: int,
    user_id: int,
    user_role: int
) -> Dict:

    if user_role == 1:  # 客户
        query = db.query(Orders).filter(Orders.client_id == user_id, Orders.is_deleted == 0)
    elif user_role == 2:  # 律师
        query = db.query(Orders).filter(Orders.lawyer_id == user_id, Orders.is_deleted == 0)
    else:
        raise HTTPException(status_code=403, detail="无效的用户角色")

    total = query.count()
    results = query.offset((page - 1) * page_size).limit(page_size).all()
    orders = [MyOrder.model_validate(o).model_dump(by_alias=True) for o in results]
    print(orders)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": orders
    }
