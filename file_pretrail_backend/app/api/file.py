import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.models.file import MyFile
from app.models.user import User
from app.services.file_service import upload_file_service  # 你可以创建一个服务来处理文件上传逻辑
from app.utils.alioss_utils import upload_to_oss
from app.utils.result_utils import ResultUtils  # 自定义工具类
from app.core.auth import get_current_user  # 获取当前用户
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    上传文件接口，用户登录后才能上传文件。
    """
    user_id = current_user.id
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")

    try:
        # 调用文件上传服务
        file_id = await upload_file_service(file, user_id, db)
        return ResultUtils.success({"data": file_id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")