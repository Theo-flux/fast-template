from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

from app.utils import set_origin_from_request

from .config import Config


async def custom_context_middleware(request, call_next):
    context["base_url"] = str(request.base_url)
    context["origin"] = set_origin_from_request(request)
    return await call_next(request)


def register_middlewares(app: FastAPI):
    allow_origins = []
    if Config.FRONTEND_URL:
        allow_origins.append(Config.FRONTEND_URL)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        expose_headers=["Set-Cookie"],
    )

    allowed_hosts = ["localhost", "127.0.0.1"]
    if Config.API_DOMAIN:
        allowed_hosts.append(Config.API_DOMAIN)
    if Config.STAGING_API_DOMAIN:
        allowed_hosts.append(Config.STAGING_API_DOMAIN)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    app.add_middleware(BaseHTTPMiddleware, dispatch=custom_context_middleware)

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
            plugins.UserAgentPlugin(),
        ),
    )
