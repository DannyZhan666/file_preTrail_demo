import os
from io import BytesIO
import oss2
from dotenv import load_dotenv
from fastapi import UploadFile

load_dotenv()  # 加载 .env 文件

# 阿里云 OSS 配置信息（假设已经配置好）
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
OSS_ACCESS_KEY = os.getenv("OSS_ACCESS_KEY")
OSS_SECRET_KEY = os.getenv("OSS_SECRET_KEY")
OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME")

def upload_to_oss(file: UploadFile, file_name: str) -> str:
    """
    上传文件到阿里云 OSS
    """
    # 创建 OSS 客户端
    auth = oss2.Auth(OSS_ACCESS_KEY, OSS_SECRET_KEY)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)

    # 读取文件内容
    file_content = file.file.read()

    # 上传到 OSS
    bucket.put_object(file_name, file_content)

    # 文件 URL（根据你的 OSS 配置，这里可能需要调整）
    file_url = f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{file_name}"

    return file_url
