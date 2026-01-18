import logging
from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4

import jwt
from fastapi import Response
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from jwt import ExpiredSignatureError, PyJWTError
from passlib.context import CryptContext

from app.database.redis import redis_client
from app.schemas.auth import TokenUserModel

from .config import Config
from .exceptions import ExpiredLink, InvalidLink, InvalidToken, RefreshTokenExpired, TokenExpired
from .logger import setup_logger

logger = setup_logger(__name__)


class Authentication:
    password_context = CryptContext(schemes=["bcrypt"])
    ACCESS_TOKEN_EXPIRY_IN_SECONDS = 900  # 15 mins
    REFRESH_TOKEN_EXPIRY_IN_SECONDS = 604800  # 7 days

    ACCOUNT_VERIFY_TOKEN_EXPIRY_IN_SECONDS = 86400  # 24 hours
    PWD_RESET_TOKEN_EXPIRY_IN_SECONDS = 3600  # 1 hour
    serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(secret_key=Config.JWT_SECRET, salt=Config.EMAIL_SALT)

    @staticmethod
    def generate_password_hash(password: str) -> str:
        return Authentication.password_context.hash(password)

    @staticmethod
    def verify_password(password: str, hash: str) -> bool:
        return Authentication.password_context.verify(password, hash)

    @staticmethod
    async def create_token(
        user_data: TokenUserModel,
        response: Optional[Response] = None,
        expiry: timedelta = None,
        refresh: bool = False,
    ) -> str:
        payload = {}

        if refresh:
            payload["user"] = user_data.model_dump(mode="json", include={"uid", "id"})
        else:
            payload["user"] = user_data.model_dump(mode="json")

        payload["exp"] = int(
            (
                datetime.now()
                + (
                    expiry
                    if expiry is not None
                    else timedelta(
                        seconds=(
                            Authentication.REFRESH_TOKEN_EXPIRY_IN_SECONDS
                            if refresh
                            else Authentication.ACCESS_TOKEN_EXPIRY_IN_SECONDS
                        )
                    )
                )
            ).timestamp()
        )
        payload["jti"] = str(uuid4())
        payload["refresh"] = refresh
        token = jwt.encode(payload=payload, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHM)

        if refresh:
            try:
                redis_key = payload["jti"]
                await redis_client.client.set(
                    name=redis_key, value=token, ex=Authentication.REFRESH_TOKEN_EXPIRY_IN_SECONDS
                )

                if response:
                    response.set_cookie(
                        key="refresh_token",
                        value=redis_key,
                        httponly=True,
                        samesite="lax" if Config.ENVIRONMENT == "development" else "none",
                        secure=Config.ENVIRONMENT != "development",
                        max_age=Authentication.REFRESH_TOKEN_EXPIRY_IN_SECONDS,
                        path="/",
                        domain=None if Config.ENVIRONMENT == "development" else f".{Config.API_DOMAIN}",
                    )

            except Exception as e:
                logging.error(f"Failed to initialize Redis client: {e}")
                pass

        return token

    @staticmethod
    async def decode_token(token: str):
        try:
            token_payload = jwt.decode(
                jwt=token,
                key=Config.JWT_SECRET,
                algorithms=[Config.JWT_ALGORITHM],
                verify=True,
            )
            return token_payload
        except ExpiredSignatureError:
            try:
                unverified_payload = jwt.decode(
                    jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM], options={"verify_exp": False}
                )
                is_refresh = unverified_payload.get("refresh", False)
                logging.warning(f"Token expired. Is refresh: {is_refresh}")

                if is_refresh:
                    logging.warning("Raising RefreshTokenExpired")
                    raise RefreshTokenExpired()
                else:
                    logging.warning("Raising TokenExpired")
                    raise TokenExpired()

            except (KeyError, ValueError, TypeError) as decode_error:
                logging.warning(f"Could not decode expired token payload: {decode_error}")
                raise TokenExpired()
            except RefreshTokenExpired:
                raise
            except TokenExpired:
                raise
        except PyJWTError:
            logging.exception("JWT decoding failed.")
            raise InvalidToken()

    @staticmethod
    async def create_url_safe_token(data: dict, exp: Optional[int] = None, url_type: str = "verify") -> str:
        try:
            token = Authentication.serializer.dumps(data)
            redis_name = f"{url_type}:{data['email']}"

            ex = (
                exp
                if exp
                else (
                    Authentication.ACCOUNT_VERIFY_TOKEN_EXPIRY_IN_SECONDS
                    if url_type == "verify"
                    else Authentication.PWD_RESET_TOKEN_EXPIRY_IN_SECONDS
                )
            )

            success = await redis_client.client.set(
                name=redis_name,
                value=token,
                ex=ex,
            )
            if not success:
                raise ValueError("Failed to store token in Redis")

            stored_token = await redis_client.client.get(redis_name)
            if stored_token != token:
                raise ValueError(f"Token verification failed for {redis_name}")

            logger.info(f"Successfully stored token in Redis for {redis_name}")

            return token
        except Exception as e:
            logging.error(f"Failed to set Redis key {redis_name}: {e}")

    @staticmethod
    async def decode_url_safe_token(token: str, url_type: str = "verify", expiry: Optional[int] = None) -> dict:
        try:
            max_age = (
                expiry
                if expiry
                else (
                    Authentication.ACCOUNT_VERIFY_TOKEN_EXPIRY_IN_SECONDS
                    if url_type == "verify"
                    else Authentication.PWD_RESET_TOKEN_EXPIRY_IN_SECONDS
                )
            )
            data = Authentication.serializer.loads(
                token,
                max_age=max_age,
            )
            return data

        except SignatureExpired:
            logging.error("Token expired")
            raise ExpiredLink()
        except BadSignature:
            logging.error("Invalid token")
            raise InvalidLink()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise InvalidLink()
