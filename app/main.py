import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.exceptions import register_exceptions
from app.core.logger import setup_logger
from app.core.middlewares import register_middlewares
from app.database.base import init_db
from app.database.redis import init_redis

app_logger = setup_logger("app.lifecycle")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle events"""
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    app_logger.info("🚀 Server starting...")
    await init_db()
    await init_redis()
    yield
    app_logger.info("👋 Server stopped...")


version = "v1"
api_version = f"/api/{version}"

app = FastAPI(
    title="FastAPI Template server",
    description="A FastAPI Template server.",
    version=version,
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/mit"},
    contact={"name": "Theo Flux", "email": "tifluse@gmail.com", "url": "https://github.com/Theo-flux/fast-template"},
    docs_url=f"{api_version}/docs",
    openapi_url=f"/api/{version}/openapi.json",
    lifespan=lifespan,
)

register_exceptions(app)
register_middlewares(app)


@app.get("/")
async def root():
    return {"message": "FastAPI Template server is running 🚀"}
