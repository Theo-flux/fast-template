from datetime import datetime
from enum import StrEnum
from typing import Generic, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

from app.core.config import Config
from app.utils.validators import email_validator, uuid_serializer

T = TypeVar("T")


class ResourceStatusModel(StrEnum):
    ACTIVE = "active"
    DEACTIVATED = "deactivated"


class GenderModel(StrEnum):
    MALE = "male"
    FEMALE = "female"


class SortOrderModel(StrEnum):
    ASC = "asc"
    DESC = "desc"


class ErrorResponse(BaseModel):
    error_code: str
    message: str


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
    def serialize_dt(self, value: datetime):
        if value:
            return value.isoformat()

    @field_serializer("uid")
    def serialize_uuid(self, value: UUID):
        return uuid_serializer(value)

    model_config = ConfigDict(from_attributes=True)


class EmailModel(BaseModel):
    email: str = Field(...)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        return email_validator(value)


class BaseFilterModel(BaseModel):
    q: Optional[str] = Field(default=None)
    limit: int = Field(
        default=Config.DEFAULT_PAGE_LIMIT, ge=Config.DEFAULT_PAGE_MIN_LIMIT, le=Config.DEFAULT_PAGE_MAX_LIMIT
    )
    offset: int = Field(default=Config.DEFAULT_PAGE_OFFSET, ge=Config.DEFAULT_PAGE_OFFSET)


class RepoFilterResponseModel(BaseModel):
    items: list
    current_page: int
    total_pages: int
    limit: int
    total: int
