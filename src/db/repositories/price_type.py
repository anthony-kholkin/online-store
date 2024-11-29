from typing import Sequence


from sqlalchemy import delete, select

from db.models.price_type import PriceType
from db.repositories.base import BaseDatabaseRepository
from schemas.price_type import PriceTypeSchema


class PriceTypeRepository(BaseDatabaseRepository):
    async def create(self, data: PriceTypeSchema) -> PriceType:
        price_type = PriceType()

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(price_type, key, value)

        self._session.add(price_type)
        await self._session.flush()

        return price_type

    async def get_all(self) -> Sequence[PriceType]:
        query_result = await self._session.execute(select(PriceType))

        return query_result.scalars().all()

    async def get_by_guid(self, guid: str) -> PriceType | None:
        return await self._session.get(PriceType, guid)

    async def update(self, instance: PriceType, data: PriceTypeSchema) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(PriceType).where(PriceType.guid == guid))
