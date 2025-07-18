import base64
from typing import Optional

from sqlalchemy.orm import Session

from app.models.file import MyFile
from app.models.job import Job
from app.models.user import User
from app.schemas.job import RawJobListForClientVO, JobDetailsForClientVO, NewJobListForClientVO, JobListForLawyerVO, \
    JobDetailsVO, NewJobListForLawyerVO, JobDetailsForAcceptVO
from app.utils.result_utils import ResultUtils
from sqlalchemy import or_


def list_raw_job_for_client(db: Session, page: int, page_size: int, client_id: int):
    # 查询 job_status = 0 和 client_id 匹配的记录
    query = db.query(Job).filter(Job.job_status == 0, Job.client_id == client_id)

    # 分页
    total = query.count()
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()

    # 转换为 RawJobListForClientVO
    job_list_for_client_vo = [
        convert_to_job_list_for_client_vo(job) for job in jobs
    ]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": job_list_for_client_vo
    }


def convert_to_job_list_for_client_vo(job: Job) -> RawJobListForClientVO:
    job_type_map = {
        0: "未分类",
        1: "房地产",
        2: "婚姻",
    }
    job_type = job_type_map.get(job.job_type, "未知类型")
    return RawJobListForClientVO(
        jobId=job.id,
        jobName=job.job_name,
        jobType=job_type,
        clientBudget=job.client_budget,
        issueDate = job.create_time
    )

def list_new_job_for_client(page: int, page_size: int, user_id: int, db: Session) -> list[NewJobListForClientVO]:
    # 获取用户角色
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("用户未找到")

    user_role = user.user_role
    query = db.query(Job).filter(Job.job_status == 1)

    if user_role == 2:  # 用户是律师
        query = query.filter(Job.lawyer_id == user_id)
    else:  # 用户是客户端
        query = query.filter(Job.client_id == user_id)

    # 分页查询
    total_jobs = query.count()
    jobs = query.offset((page - 1) * page_size).limit(page_size).all()

    # 转换 Job 为 NewJobListForClientVO
    job_list_for_client = [convert_to_new_job_list_for_client_vo(job, db) for job in jobs]


    return job_list_for_client

def convert_to_new_job_list_for_client_vo(job: Job, db: Session) -> NewJobListForClientVO:
    # 转换 MyJob 到 NewJobListForClientVO
    new_job_vo = NewJobListForClientVO(
        job_id=job.id,
        job_name=job.job_name,
        job_type=job.job_type,
        client_budget=job.client_budget,
        due=job.due,
        lawyer_budget=job.lawyer_budget,
        due_law=job.due_law,
        issue_date=job.create_time,
        update_date=job.update_time,
    )

    # 查询律师的姓名
    lawyer: Optional[User] = db.query(User).filter(User.id == job.lawyer_id).first()
    if lawyer:
        new_job_vo.lawyer_name = lawyer.username

    return new_job_vo

def list_raw_job_for_lawyer(page: int, page_size: int, lawyer_id: int, db: Session) -> list[JobListForLawyerVO]:
    # 获取 status = 0 的工单（没有分配律师）
    job_list_no_status = db.query(Job).filter(Job.job_status == 0).all()

    # 获取 status = 1 的工单，并且检查是否律师已经参与
    job_list_yes_status = db.query(Job).filter(Job.job_status == 1, Job.lawyer_id == lawyer_id).all()

    # 获取所有 job_name（状态为1的工单的 job_name）
    job_name_yes_status = {job.job_name for job in job_list_yes_status}

    # 筛选出 job_status = 0 的工单，且其 job_name 不在 job_name_yes_status 中
    remaining_jobs = [job for job in job_list_no_status if job.job_name not in job_name_yes_status]

    # 批量转换 Job -> JobListForLawyerVO
    job_list_for_lawyer = [convert_to_job_list_for_lawyer_vo(job, db) for job in remaining_jobs]

    return job_list_for_lawyer

def convert_to_job_list_for_lawyer_vo(job: Job, db: Session) -> JobListForLawyerVO:
    # 转换 MyJob 到 JobListForLawyerVO
    job_vo = JobListForLawyerVO(
        job_id=job.id,
        job_name=job.job_name,
        job_type=job.job_type,
        client_budget=job.client_budget,
        issue_date=job.create_time,
    )

    # 查询客户端的名称
    client: Optional[User] = db.query(User).filter(User.id == job.client_id).first()
    if client:
        job_vo.client_name = client.username

    return job_vo

def list_new_job_for_lawyer(page: int, page_size: int, lawyer_id: int, db: Session) -> list[NewJobListForLawyerVO]:
    # 获取 status = 2 且 lawyer_id = userId 的工单
    new_job_list = db.query(Job).filter(Job.job_status == 2, Job.lawyer_id == lawyer_id).all()

    # 批量转换 Job -> NewJobListForLawyerVO
    job_list_for_lawyer = [convert_to_new_job_list_for_lawyer_vo(job, db) for job in new_job_list]

    return job_list_for_lawyer

def convert_to_new_job_list_for_lawyer_vo(job: Job, db: Session) -> NewJobListForLawyerVO:
    # 转换 MyJob 到 NewJobListForLawyerVO
    job_vo = NewJobListForLawyerVO(
        job_id=job.id,
        job_name=job.job_name,
        job_type=job.job_type,
        job_intro=job.job_intro,
        client_budget=job.client_budget,
        issue_date=job.create_time,
        update_time=job.update_time
    )

    # 查询客户端的名称
    client: Optional[User] = db.query(User).filter(User.id == job.client_id).first()
    if client:
        job_vo.client_name = client.username

    return job_vo

def details(job_id: int, user_id: int, db: Session) -> Optional[JobDetailsVO]:
    # 获取工单信息
    my_job: Optional[Job] = db.query(Job).filter(Job.id == job_id).first()
    if not my_job:
        return None

    # 创建 JobDetailsVO 对象并填充字段
    job_details = JobDetailsVO(
        job_id=my_job.id,
        job_name=my_job.job_name,
        job_type=my_job.job_type,
        job_intro=my_job.job_intro,
        client_id=my_job.client_id,
        client_budget=my_job.client_budget,
        expected_time=my_job.due,
        issue_date=my_job.create_time
    )

    # 查询客户端信息
    client: Optional[User] = db.query(User).filter(User.id == my_job.client_id).first()
    if client:
        job_details.client_name = client.username

    # 获取文件信息并转为 Base64 编码
    my_file: Optional[MyFile] = db.query(MyFile).filter(MyFile.id == my_job.file_id).first()
    if my_file:
        job_details.file_content = base64.b64encode(my_file.content).decode('utf-8')
        job_details.path = my_file.path
        job_details.file_name = my_file.file_name

    return job_details

def details_for_client(id: int, db: Session, current_user_id: int) -> JobDetailsForClientVO:
    # 查询工单
    my_job: Optional[Job] = db.query(Job).filter(Job.id == id).first()
    if not my_job:
        raise ValueError("工单未找到")

    # 获取工单的详细信息
    job_details = JobDetailsForClientVO(
        job_id=my_job.id,
        job_name=my_job.job_name,
        job_type=my_job.job_type,
        job_intro=my_job.job_intro,
        client_id=my_job.client_id,
        client_budget=my_job.client_budget,
        issue_date=my_job.create_time,
        update_time=my_job.update_time,
        due=my_job.due,
        due_law=my_job.due_law,
        lawyer_id=my_job.lawyer_id,
        lawyer_budget=my_job.lawyer_budget,
        lawyer_comment=my_job.lawyer_comment,
    )

    # 获取 Client Name
    client: Optional[User] = db.query(User).filter(User.id == my_job.client_id).first()
    if client:
        job_details.client_name = client.username

    # 获取 Lawyer Name
    lawyer: Optional[User] = db.query(User).filter(User.id == my_job.lawyer_id).first()
    if lawyer:
        job_details.lawyer_name = lawyer.username

    # 获取文件内容并转为 base64 编码
    my_file: Optional[MyFile] = db.query(MyFile).filter(MyFile.id == my_job.file_id).first()
    if my_file:
        job_details.file_content = base64.b64encode(my_file.content).decode("utf-8")
        job_details.path = my_file.path
        job_details.file_name = my_file.file_name

    return job_details

def details_for_accept(job_id: int, user_id: int, db: Session) -> Optional[JobDetailsForAcceptVO]:
    # 获取工单信息
    my_job: Optional[Job] = db.query(Job).filter(Job.id == job_id).first()
    if not my_job:
        return None

    # 创建 JobDetailsForAcceptVO 对象并填充字段
    job_details = JobDetailsForAcceptVO(
        job_id=my_job.id,
        job_name=my_job.job_name,
        job_type=my_job.job_type,
        job_intro=my_job.job_intro,
        client_id=my_job.client_id,
        client_budget=my_job.client_budget,
        issue_date=my_job.create_time
    )

    # 查询客户端信息
    client: Optional[User] = db.query(User).filter(User.id == my_job.client_id).first()
    if client:
        job_details.client_account = client.user_account
        job_details.client_name = client.username
        job_details.client_phone = client.phone
        job_details.client_email = client.email

    # 获取文件信息并转为 Base64 编码
    my_file: Optional[MyFile] = db.query(MyFile).filter(MyFile.id == my_job.file_id).first()
    if my_file:
        job_details.file_content = base64.b64encode(my_file.content).decode('utf-8')
        job_details.path = my_file.path
        job_details.file_name = my_file.file_name

    return job_details

