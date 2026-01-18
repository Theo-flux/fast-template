from typing import Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer
from sqlalchemy.sql.selectable import Select

from app.schemas.base import EmailModel, GenderModel
from app.utils.validators import uuid_serializer

T = TypeVar("T")
SelectOfScalar = Select[T]


class SetPwdModel(EmailModel):
    new_password: str


class ChangePwdModel(BaseModel):
    old_password: str
    new_password: str


class TokenModel(BaseModel):
    access_token: str
    is_email_verified: bool


class ResetPwdModel(BaseModel):
    token: str
    new_password: str


class TokenUserModel(BaseModel):
    id: int
    uid: UUID
    first_name: str
    last_name: str
    email: str
    gender: str
    phone_number: str
    is_email_verified: bool
    is_number_verified: bool

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID):
        return uuid_serializer(value)

    model_config = ConfigDict(from_attributes=True)


class UserLoginModel(EmailModel):
    password: str = Field(...)


class UserCreateModel(EmailModel):
    password: str = Field(...)
    first_name: str = Field(...)
    last_name: str = Field(...)
    phone_number: str = Field(...)
    gender: GenderModel = Field(...)
    interests: list[str] = Field(...)


class UpdateUserModel(BaseModel):
    is_email_verified: Optional[bool] = Field(default=None)
    interests: Optional[list[str]] = Field(default=None)
    avatar: Optional[UUID] = Field(default=None)
    banner: Optional[UUID] = Field(default=None)
    old_password: Optional[str] = Field(default=None)
    new_password: Optional[str] = Field(default=None)
