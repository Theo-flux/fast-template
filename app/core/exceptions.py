from typing import Callable, Optional

from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.core.logger import setup_logger
from app.schemas.base import ErrorResponse

logger = setup_logger(__name__)


class AppException(Exception):
    """The base class for handling exceptions around the app."""

    def __init__(self, message: Optional[str] = None):
        self.message = message
        super().__init__(message)


class InvalidToken(AppException):
    """This handles user invalid token exceptions"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "This token is invalid or expired. Pls get a new token.")


class ResourceExists(AppException):
    """Raised when a required resource already exists in database"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Resource already exists.")


class NotFound(AppException):
    """Raised when a required resource doesn't exist in database"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Resource doesn't exist.")


class InActive(AppException):
    """Raised when a required resource is inactive in the database"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Resource is inactive.")


class UserEmailExists(AppException):
    """This handles user email exists"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "User with email already exist.")


class UserPhoneNumberExists(AppException):
    """This handles user phone number exists"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "User with phone number already exists.")


class WrongCredentials(AppException):
    """This handles wrong user email or password."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Wrong email or password.")


class TokenExpired(AppException):
    """This handles expired user token."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Token has expired.")


class AccessTokenRequired(AppException):
    """This handles expired user token."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Provide an access token.")


class RefreshTokenRequired(AppException):
    """This handles expired user token."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Provide a refresh token.")


class RefreshTokenExpired(AppException):
    """This handles expired user token."""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "E402")


class ExpiredLink(AppException):
    """This handles expired password reset token"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Link expired. get a new one.")


class InvalidLink(AppException):
    """This handles invalid password reset token"""

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or "Link is invalid. get a new one.")


class InsufficientPermissions(AppException):
    """Raised when user doesn't have required role/permissions"""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "You don't have permission to access this resource."
        super().__init__(self.message)


class BadRequest(AppException):
    """Raised when a bad request is made to the api."""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "Bad request"
        super().__init__(self.message)


class UserNotVerified(AppException):
    """Raised when an unverified user calls an endpoint."""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "Your email is not verified."
        super().__init__(self.message)


class UserSameOldPwd(AppException):
    """Raised when a user tries to change new password with similar old password."""

    def __init__(self, message: Optional[str] = None):
        self.message = message or "New password cannot be same as old password."
        super().__init__(self.message)


def create_exception_handler(
    status_code: int, default_message: str = "An error occurred"
) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(req: Request, exc: AppException) -> JSONResponse:
        message = getattr(exc, "message", default_message)
        logger.warning(f"{exc.__class__.__name__}: {message} | Path: {req.url.path}")
        response = ErrorResponse(error_code=exc.__class__.__name__, message=message)
        return JSONResponse(status_code=status_code, content=response.model_dump())

    return exception_handler


def register_exceptions(app: FastAPI):
    status_map = {
        InvalidToken: status.HTTP_401_UNAUTHORIZED,
        TokenExpired: status.HTTP_401_UNAUTHORIZED,
        AccessTokenRequired: status.HTTP_401_UNAUTHORIZED,
        RefreshTokenRequired: status.HTTP_410_GONE,
        RefreshTokenExpired: status.HTTP_410_GONE,
        ExpiredLink: status.HTTP_410_GONE,
        InvalidLink: status.HTTP_410_GONE,
        NotFound: status.HTTP_404_NOT_FOUND,
        InActive: status.HTTP_404_NOT_FOUND,
        WrongCredentials: status.HTTP_404_NOT_FOUND,
        ResourceExists: status.HTTP_409_CONFLICT,
        UserEmailExists: status.HTTP_409_CONFLICT,
        UserPhoneNumberExists: status.HTTP_409_CONFLICT,
        UserNotVerified: status.HTTP_403_FORBIDDEN,
        InsufficientPermissions: status.HTTP_405_METHOD_NOT_ALLOWED,
        BadRequest: status.HTTP_400_BAD_REQUEST,
        UserSameOldPwd: status.HTTP_400_BAD_REQUEST,
    }

    for exc, code in status_map.items():
        app.add_exception_handler(exc, create_exception_handler(code))

    @app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
    async def internal_server_error(request: Request, exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "A 500 error exception occurred!",
                "error_code": "InternalServerError",
            },
        )
