import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.exceptions import register_exceptions
from src.core.logger import setup_logger
from src.core.middlewares import register_middlewares
from src.db.base import init_db
from src.db.redis import init_redis

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

app = FastAPI(
    title="FastAPI Template",
    description="A REST API Template with authentication fully implemented and custom email templates.",
    version=version,
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/mit"},
    contact={"name": "Theo Flux", "email": "tifluse@gmail.com", "url": "https://github.com/Theo-flux/fast-template"},
    docs_url=f"/api/{version}/docs",
    openapi_url=f"/api/{version}/openapi.json",
    lifespan=lifespan,
)

register_exceptions(app)
register_middlewares(app)


@app.get("/")
async def root():
    return {"message": "Fastapi template server is running 🚀"}
