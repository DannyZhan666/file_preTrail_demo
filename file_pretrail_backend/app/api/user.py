import re
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.core.database import SessionLocal, get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, LawyerResponse
from app.schemas.user import User as UserSchema  # 引入Pydantic用户模型
from app.services.user_service import get_lawyers
from app.utils.page_help import paginate
from app.utils.result_utils import ResultUtils

router = APIRouter(prefix="/user", tags=["用户模块"])


@router.post("/register")
def register(user:
UserRegister, db: Session = Depends(get_db)):
    if user.user_password != user.check_password:
        raise HTTPException(status_code=400, detail="两次密码输入不一致")

    # 检查特殊字符
    if re.search(r"[`~!@#$%^&*()+=|{}':;,\[\].<>/?~！@#￥……&*（）——+|{}【】‘；：”“’。，、？]", user.user_account):
        raise HTTPException(status_code=400, detail="用户名不能包含特殊字符")

    # 账号重复检查
    existing_user = db.query(User).filter(User.user_account == user.user_account).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="账号已存在")

    hashed_password = get_password_hash(user.user_password)
    new_user = User(
        user_account=user.user_account,
        user_password=hashed_password,
        user_role=user.user_role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ResultUtils.success({"id": new_user.id, "message": "注册成功"})


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_account == login_data.userAccount).first()
    if not db_user or not verify_password(login_data.userPassword, db_user.user_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 生成 JWT Token
    access_token = create_access_token(data={"user_id": db_user.id})

    # 使用 ResultUtils 返回统一响应格式
    return ResultUtils.success({
        "userRole": db_user.user_role,
        "access_token": access_token,
        "token_type": "bearer"
    })


@router.post("/logout")
def logout():
    return {"message": "登出成功（前端请删除 token）"}


@router.get("/current")
def get_current_user_data(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的信息
    - 通过JWT验证用户身份
    - 查询数据库获取详细信息
    """
    # 你可以在这里对用户进行进一步校验（如果有必要）
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户未登录")

    # 假设你已经有了查询用户的方法
    user_data = {
        "id": current_user.id,
        "username": current_user.username,
        "userAccount": current_user.user_account,
        "gender": current_user.gender,
        "avatarUrl": current_user.avatar_url,
        "phone": current_user.phone,
        "email": current_user.email,
        "userRole": current_user.user_role,
        "createTime": current_user.create_time,
    }

    return ResultUtils.success(user_data)


@router.get("/lawyerList")
def get_lawyer_list(page: int, pageSize: int, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    """
    获取律师列表，支持分页
    """
    user_id = current_user.id
    # Use the service to get the paginated lawyer data
    paginated_data = get_lawyers(db, user_id, page, pageSize)

    if not paginated_data:
        raise HTTPException(status_code=404, detail="User not found or no lawyers available")

    lawyer_list = [LawyerResponse.model_validate(lawyer.__dict__) for lawyer in paginated_data["list"]]

    return ResultUtils.success({
        "page": page,
        "page_size": pageSize,
        "total": paginated_data["total"],
        "data": lawyer_list
    })
