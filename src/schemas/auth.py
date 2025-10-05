from enum import StrEnum
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel, field_serializer
from sqlalchemy.sql.selectable import Select

from src.schemas import EmailModel
from src.utils.validators import uuid_serializer

T = TypeVar("T")
SelectOfScalar = Select[T]


class UserType(StrEnum):
    NEW_USER = "new_user"
    OLD_USER = "old_user"


class SetPwdModel(EmailModel):
    new_password: str


class ChangePwdModel(BaseModel):
    old_password: str
    new_password: str


class TokenModel(BaseModel):
    access_token: str
    is_email_verified: bool
    user_type: UserType


class TokenUserModel(BaseModel):
    id: int
    uid: UUID
    staff_no: str
    first_name: str
    last_name: str
    email: str
    status: str

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID, _info):
        return uuid_serializer(value)
