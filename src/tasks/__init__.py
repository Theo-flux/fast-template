from celery import Celery

from src.core.config import Config

if Config.REDIS_PASSWORD:
    redis_url = f"redis://:{Config.REDIS_PASSWORD}@{Config.REDIS_HOST}:{Config.REDIS_PORT}"
else:
    redis_url = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}"

celery_app = Celery(
    "worker",
    broker=f"{redis_url}/1",
    backend=f"{redis_url}/2",
)

celery_app.autodiscover_tasks(["src.tasks"])
