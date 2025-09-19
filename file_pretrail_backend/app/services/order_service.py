from sqlalchemy.orm import Session
from typing import Dict, List
from fastapi import HTTPException

from app.models.job import Job
from app.models.newjob import NewJob
from app.models.orders import Orders
from app.models.user import User
from app.schemas.order import MyOrder, OrderCreateRequest, OrderForLaywerVO, OrderForClientVO


def order_list_lawyer(db: Session,page: int, page_size: int, user_id: int):

    query = db.query(Orders).filter(Orders.lawyer_id == user_id, Orders.is_deleted == 0)
    total = query.count()
    results = query.order_by(Orders.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
    # 转换为 OrderVO
    orders = []
    for order in results:
        client = db.query(User).filter(User.id == order.client_id).first()  # 获取客户信息
        newJob = db.query(NewJob).filter(NewJob.id == order.new_jid).first()  # 获取工单信息
        if client:
            order_for_lawyer_vo = OrderForLaywerVO(
                id=order.id,
                order_name=order.order_name,
                client_name=client.username,  # 假设客户名存储在 User 表的 name 字段
                create_time=order.create_time,
                client_due_date=newJob.due,  # 假设客户期限字段为 client_due_date
                lawyer_due_date=newJob.due_law  # 假设律师期限字段为 lawyer_due_date
            )
            orders.append(order_for_lawyer_vo)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": orders
    }

def order_list_client(db: Session,page: int, page_size: int, user_id: int):

    query = db.query(Orders).filter(Orders.client_id == user_id, Orders.is_deleted == 0)
    total = query.count()
    results = query.order_by(Orders.create_time.desc()).offset((page - 1) * page_size).limit(page_size).all()
    # 转换为 OrderVO
    orders = []
    for order in results:
        lawyer = db.query(User).filter(User.id == order.lawyer_id).first()  # 获取客户信息
        newJob = db.query(NewJob).filter(NewJob.id == order.new_jid).first()  # 获取工单信息
        if lawyer:
            order_for_client_vo = OrderForClientVO(
                id=order.id,
                order_name=order.order_name,
                lawyer_name=lawyer.username,  # 假设客户名存储在 User 表的 name 字段
                create_time=order.create_time,
                client_due_date=newJob.due,  # 假设客户期限字段为 client_due_date
                lawyer_due_date=newJob.due_law  # 假设律师期限字段为 lawyer_due_date
            )
            orders.append(order_for_client_vo)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": orders
    }


def create_order(order_create_request: OrderCreateRequest, user_id: int, db: Session) -> int:

    # 获取与工单关联的 MyJob 信息
    job = db.query(NewJob).filter(NewJob.id == order_create_request.new_jid).first()
    if not job:
        return -1  # 如果工单不存在，返回失败

    # 创建订单对象
    my_order = Orders(
        order_name=order_create_request.order_name,
        new_jid=order_create_request.new_jid,
        origin_jid=order_create_request.origin_jid,
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
