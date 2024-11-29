import json

from fastapi import Depends
from redis.asyncio import Redis

from db.redis import get_redis
from schemas.outlet import OutletSchema


class OutletRedisRepository:
    def __init__(self, session: Redis = Depends(get_redis)) -> None:
        self._session = session

    async def set_list(
        self,
        token: str,
        models: list[OutletSchema],
        expiration_seconds: int | None = None,
    ) -> str:
        value = json.dumps([model.model_dump() for model in models])

        if expiration_seconds:
            await self._session.setex(name=token, time=expiration_seconds, value=value)
        else:
            await self._session.set(name=token, value=value)

        return token

    async def get_list(self, token: str | None) -> list[OutletSchema] | None:
        if not isinstance(token, str) or not token:
            return None

        data = await self._session.get(token)

        if data is None:
            return None

        return [OutletSchema(**item) for item in json.loads(data)]

    async def delete(self, token: str) -> None:
        await self._session.delete(token)
