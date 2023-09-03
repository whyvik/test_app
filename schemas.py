import json
from typing import List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID
from datetime import date, datetime


class TaskSchema(BaseModel):
    task_sum: Optional[int] = None
    task_date: Optional[date] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True


class RequestTask(BaseModel):
    parameter: TaskSchema = Field(...)


class UserSchema(BaseModel):
    user_uuid: UUID = Field(default_factory=uuid4)
    email: Optional[str] = None
    hashed_password: Optional[str] = None

    class Config:
        from_attributes = True


class RequestUser(BaseModel):
    email: Optional[str] = None
    hashed_password: Optional[str] = None


class Token(BaseModel):
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return json.JSONEncoder.default(self, obj)
