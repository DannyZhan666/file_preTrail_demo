from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegister


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
