from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegister
from app.utils.page_help import paginate


def create_user(db: Session, user: UserRegister):
    db_user = User(
        user_account=user.user_account,
        user_password=user.user_password,
        username=user.username,
        email=user.email,
        phone=user.phone
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_lawyers(db: Session, user_id: int, page: int, page_size: int):
    # Get the user role from the db if necessary
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None  # or raise an exception

    # Query for lawyers
    query = db.query(User).filter(User.user_role == 2, User.is_deleted == 0)
    return paginate(query, page, page_size)