from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config import Base
from uuid import uuid4
import datetime


class Task(Base):
    __tablename__ = "tasks"
    task_uuid = Column(UUID(as_uuid=True),
                       unique=True,
                       default=uuid4,
                       primary_key=True,
                       index=True)
    task_sum = Column(Integer)
    task_date = Column(DateTime(timezone=False),
                       default=datetime.datetime.utcnow)
    category = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.user_uuid'))
    # owner = relationship("Users", back_populates="tasks")


class Users(Base):
    __tablename__ = "users"
    user_uuid = Column(UUID(as_uuid=True),
                       unique=True,
                       default=uuid4,
                       primary_key=True,
                       index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    # tasks = relationship("Task", back_populates="owner")




