from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from src.utils.validators import email_validator, uuid_serializer

T = TypeVar("T")


class ServerRespModel(BaseModel, Generic[T]):
    data: T
    message: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PaginationModel(BaseModel):
    total: int
    current_page: int
    limit: int
    total_pages: int


class PaginatedResponseModel(BaseModel, Generic[T]):
    items: list[T]
    pagination: PaginationModel


class ServerErrorModel(BaseModel, Generic[T]):
    error_code: T
    message: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DBModel(BaseModel):
    uid: UUID
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID, _info):
        return uuid_serializer(value)

    model_config = ConfigDict(from_attributes=True)


class EmailModel(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return email_validator(value)
