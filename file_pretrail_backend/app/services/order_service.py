from sqlalchemy.orm import Session
from typing import Dict, List
from fastapi import HTTPException

from app.models.job import Job
from app.models.orders import Orders
from app.schemas.order import MyOrder, OrderCreateRequest


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


def create_order(order_create_request: OrderCreateRequest, user_id: int, db: Session) -> int:

    # 获取与工单关联的 MyJob 信息
    job = db.query(Job).filter(Job.id == order_create_request.job_id).first()
    if not job:
        return -1  # 如果工单不存在，返回失败

    # 创建订单对象
    my_order = Orders(
        order_name=order_create_request.order_name,
        jid=order_create_request.job_id,
        client_id = job.client_id,
        lawyer_id = job.lawyer_id,
    )
    # # 设置订单的客户和律师信息
    # my_order.
    # my_order.lawyer_id = job.lawyer_id

    # 保存订单信息
    db.add(my_order)
    db.commit()

    return 1  # 返回成功标识
