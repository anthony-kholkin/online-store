from fastapi import Depends

from core.exceptions import (
    good_not_found_exception,
)
from db.models import Good
from db.repositories.good import GoodRepository
from services.base.base import BaseService


class BaseGoodService(BaseService):
    def __init__(
        self,
        good_repository: GoodRepository = Depends(),
    ):
        self._good_repository = good_repository

    async def get_by_guid(self, guid: str) -> Good:
        good = await self._good_repository.get_by_guid(guid=guid)

        if not good:
            raise good_not_found_exception

        return good
