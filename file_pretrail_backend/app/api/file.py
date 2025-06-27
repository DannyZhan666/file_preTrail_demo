from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.file_service import upload_file_service  # 你可以创建一个服务来处理文件上传逻辑
from app.utils.result_utils import ResultUtils  # 自定义工具类
from app.core.auth import get_current_user  # 获取当前用户
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


@router.post("/upload", response_model=int)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db),
                      current_user: dict = Depends(get_current_user)):
    # 用户校验
    if not current_user:
        raise HTTPException(status_code=401, detail="未登录")

    # 调用上传文件的服务
    try:
        file_id = await upload_file_service(file, current_user['id'], db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

    return ResultUtils.success(file_id)  # 返回上传成功的文件 ID
