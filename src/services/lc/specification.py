from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import specification_not_found_exception
from db.models import Specification
from db.repositories.specification import SpecificationRepository
from db.session import get_session
from schemas.specification import (
    SpecificationSchema,
)


class SpecificationService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        specification_repository: SpecificationRepository = Depends(),
    ):
        self._session = session
        self._specification_repository = specification_repository

    async def get_by_guid(self, guid: str) -> Specification:
        specification = await self._specification_repository.get_by_guid(guid=guid)

        if not specification:
            raise specification_not_found_exception

        return specification

    async def merge_batch(self, data: list[SpecificationSchema]) -> list[Specification]:
        return await self._specification_repository.merge_batch(data=data)

    async def create_batch(self, data: list[SpecificationSchema]) -> list[Specification]:
        return await self._specification_repository.create_batch(data=data)

    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        return await self._specification_repository.get_by_good_guid(good_guid=good_guid)
