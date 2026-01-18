import logging
from typing import Any, Dict, Optional, Union

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.authentication import Authentication
from app.core.exceptions import AccessTokenRequired, InvalidToken, RefreshTokenExpired, TokenExpired
from app.database.redis import redis_client


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True, is_not_protected: bool = False):
        self.is_not_protected = is_not_protected
        super().__init__(
            auto_error=auto_error,
        )

    async def is_token_valid(self, token: str) -> Union[Dict[str, Any], bool]:
        try:
            token_payload = await Authentication.decode_token(token)

            if await redis_client.in_blocklist(token_payload["jti"]):
                raise InvalidToken()

            return token_payload
        except RefreshTokenExpired as e:
            logging.warning(f"RefreshTokenExpired caught in is_token_valid: {e}")
            raise
        except TokenExpired as e:
            logging.warning(f"TokenExpired caught in is_token_valid: {e}")
            raise
        except Exception as e:
            logging.warning(f"Other exception in is_token_valid: {type(e).__name__}: {e}")
            return False

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        auth_header = request.headers.get("Authorization")

        if self.is_not_protected and not auth_header:
            return None

        cred = await super().__call__(request)
        token = cred.credentials

        token_payload = await self.is_token_valid(token)
        if not token_payload:
            raise InvalidToken()

        await self.verify_token_data(token_payload)
        return token_payload

    async def verify_token_data(self, token_payload) -> None:
        raise NotImplementedError("Please override this method in child classes.")


class AccessTokenBearer(TokenBearer):
    async def verify_token_data(self, token_payload):
        if token_payload and token_payload["refresh"]:
            raise AccessTokenRequired()
