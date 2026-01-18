from typing import Optional

import backoff
import redis.asyncio as aioredis
from redis.asyncio.retry import Retry
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError, RedisError

from app.core.config import Config
from app.core.logger import setup_logger

logger = setup_logger(__name__)


class RedisClient:
    _instance: Optional["RedisClient"] = None
    _client: Optional[aioredis.Redis] = None
    _BLOCKED_PREFIX = "blocked"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init(self):
        """Initialize Redis connection with retries"""
        if self._client is None:
            try:
                retry = Retry(ExponentialBackoff(), 3)
                url = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
                if Config.REDIS_PASSWORD:
                    url = f"redis://:{Config.REDIS_PASSWORD}@{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
                self._client = aioredis.from_url(
                    url=url,
                    retry=retry,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5,
                    health_check_interval=30,
                )
                # Test connection
                await self._client.ping()
                logger.info("Successfully connected to Redis")
            except ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self._client = None
                raise
            except Exception as e:
                logger.error(f"Unexpected error connecting to Redis: {e}")
                self._client = None
                raise

    @property
    def client(self) -> Optional[aioredis.Redis]:
        return self._client

    async def close(self):
        """Close Redis connection"""
        if self._client:
            await self._client.close()
            self._client = None

    @backoff.on_exception(backoff.expo, (ConnectionError, RedisError), max_tries=3, max_time=30)
    async def add_to_blocklist(self, key: str, expiry: int = 3600) -> bool:
        """Add token to blocklist with retry mechanism"""
        if not self._client:
            logger.warning("Redis client not initialized")
            return False

        try:
            await self._client.set(name=f"{self._BLOCKED_PREFIX}:{key}", value="", ex=expiry)
            return True
        except Exception as e:
            logger.error(f"Error adding to blocklist: {e}")
            raise

    async def in_blocklist(self, key: str) -> bool:
        """Check if token is in blocklist"""
        if not self._client:
            logger.warning("Redis client not initialized")
            return False

        try:
            return await self._client.exists(f"{self._BLOCKED_PREFIX}:{key}") > 0
        except Exception as e:
            logger.error(f"Error checking blocklist: {e}")
            return False


redis_client = RedisClient()


async def init_redis() -> bool:
    """Initialize Redis connection with detailed status logging"""
    try:
        logger.info(f"🔄 Connecting to Redis at {Config.REDIS_HOST}:{Config.REDIS_PORT}...")
        await redis_client.init()

        # Verify connection with PING
        if await redis_client.client.ping():
            logger.info("✅ Redis connection established successfully")

            # Log Redis server info
            info = await redis_client.client.info()
            logger.info(f"📊 Redis Version: {info.get('redis_version')}")
            logger.info(f"💾 Memory Used: {info.get('used_memory_human')}")
            return True

    except ConnectionError as e:
        logger.warning(f"⚠️  Redis connection failed: {e}")
        logger.info("💡 Application will continue without Redis features")
    except Exception as e:
        logger.error(f"❌ Unexpected Redis error: {e}")
        logger.info("💡 Application will continue without Redis features")

    return False
