import functools
import typing

from redis.asyncio import Redis, from_url

from core.config import settings


@functools.lru_cache
def get_redis_connection() -> Redis:
    return from_url(settings().REDIS_DSN, encoding="utf-8", decode_responses=True)  # type: ignore


async def get_redis() -> typing.AsyncGenerator[Redis, None]:
    async with get_redis_connection() as redis:
        yield redis
