import re
from datetime import datetime
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status, UploadFile, File
from sqlalchemy.orm import Session

from app.core.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.core.database import SessionLocal, get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, LawyerResponse, UpdateUserRequest
from app.schemas.user import User as UserSchema  # 引入Pydantic用户模型
from app.services.user_service import get_lawyers, upload_avatar
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


@router.put("/update")
async def update_user_info(update_data: UpdateUserRequest,db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    更新用户信息接口
    """

    # 获取用户
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户信息
    if update_data.username:
        user.username = update_data.username
    if update_data.gender is not None:
        user.gender = update_data.gender
    if update_data.avatarUrl:
        user.avatar_url = update_data.avatarUrl
    if update_data.phone:
        user.phone = update_data.phone
    if update_data.email:
        user.email = update_data.email

    # 提交数据库更新
    db.commit()

    # 刷新用户对象，确保获取最新的用户数据
    db.refresh(user)

    return {"code": 200, "msg": "用户信息更新成功", "data": user}


@router.put("/avatar")
async def upload_avatar_api(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    上传用户头像接口
    """

    # 获取用户
    user = db.query(User).filter(User.id == current_user.id).first()

    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用 user_service 中的 upload_avatar 方法处理头像上传
        avatar_url = upload_avatar(file, user_id, db)

        return {"code": 200, "msg": "头像上传成功", "data": {"avatarUrl": avatar_url}}

    except HTTPException as e:
        raise e  # 直接抛出 HTTPException 错误
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")
