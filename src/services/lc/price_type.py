from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import price_type_not_found_exception
from db.models.price_type import PriceType
from db.repositories.price_type import PriceTypeRepository
from db.session import get_session
from schemas.price_type import PriceTypeSchema


class PriceTypeService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        price_type_repository: PriceTypeRepository = Depends(),
    ):
        self._session = session
        self._price_type_repository = price_type_repository

    async def get_all(self) -> Sequence[PriceType]:
        return await self._price_type_repository.get_all()

    async def get_by_guid(self, guid: str) -> PriceType:
        price_type = await self._price_type_repository.get_by_guid(guid=guid)

        if not price_type:
            raise price_type_not_found_exception

        return price_type

    async def create(self, data: PriceTypeSchema) -> PriceType:
        price_type = await self._price_type_repository.create(data=data)

        return price_type

    async def update(self, guid: str, data: PriceTypeSchema) -> PriceType:
        price_type = await self.get_by_guid(guid=guid)

        await self._price_type_repository.update(instance=price_type, data=data)
        await self._session.commit()

        return price_type

    async def create_or_update(self, data: PriceTypeSchema) -> PriceType:
        price_type = await self._price_type_repository.get_by_guid(guid=data.guid)

        if not price_type:
            price_type = await self.create(data=data)
        else:
            price_type = await self.update(guid=data.guid, data=data)

        await self._session.commit()

        return price_type

    async def delete(self, guid: str) -> None:
        await self.get_by_guid(guid=guid)

        await self._price_type_repository.delete(guid=guid)
        await self._session.commit()
