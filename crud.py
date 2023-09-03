import json
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM
from jose import jwt
from sqlalchemy.orm import Session
from models import Task, Users
from schemas import TaskSchema, UUIDEncoder
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

# SECRET_KEY = '3c2b0d72762289e1108dba406130ec8474312ee065b7d5668f9d533eed887e5a'
# ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/')


def get_task(db: Session, current_user):
    return db.query(Task).filter(Task.owner_id == UUID(current_user["id"][1:-1])).all()


def create_task(db: Session, task: TaskSchema, current_user):
    _task = Task(task_sum=task.task_sum,
                 task_date=task.task_date,
                 category=task.category,
                 owner_id=UUID(current_user["id"][1:-1]))

    db.add(_task)
    db.commit()
    db.refresh(_task)
    return _task


def create_user(db: Session, email: str, password: str):
    _user = Users(email=email,
                  hashed_password=bcrypt_context.hash(password))
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


def authenticate_user(email: str, password: str, db):
    _user = db.query(Users).filter(Users.email == email).first()
    if not _user:
        return create_user(db, email, password)
    if not bcrypt_context.verify(password, _user.hashed_password):
        return False
    return _user


def create_access_token(email: str, user_uuid: int, expires_delta: timedelta):
    encode = {'sub': email, 'id': json.dumps(user_uuid, cls=UUIDEncoder)}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
