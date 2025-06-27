from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import RawJobListForClientVO
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
