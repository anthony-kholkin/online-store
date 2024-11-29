from fastapi import Depends

from core.exceptions import (
    invalid_creds_exception,
)
from db.repositories.outlet import OutletRedisRepository
from schemas.outlet import OutletSchema


class OutletService:
    def __init__(
        self,
        outlet_repository: OutletRedisRepository = Depends(),
    ):
        self._outlet_repository = outlet_repository

    async def get_all_by_token(self, token: str | None) -> list[OutletSchema]:
        outlets = await self._outlet_repository.get_list(token=token)

        if outlets is None:
            raise invalid_creds_exception

        return outlets

    async def set_list(
        self,
        token: str,
        outlets: list[OutletSchema],
        expiration_seconds: int | None = None,
    ) -> str:
        """Записывает пару токен - список торговых точек."""

        return await self._outlet_repository.set_list(
            token=token, models=outlets, expiration_seconds=expiration_seconds
        )
