from typing import Sequence


from sqlalchemy import select

from db.models import GoodStorage
from db.repositories.base import BaseDatabaseRepository
from schemas.good_storage import GoodStorageCreateSchema


class GoodStorageRepository(BaseDatabaseRepository):
    async def get_all(self) -> Sequence[GoodStorage]:
        query_result = await self._session.execute(select(GoodStorage))

        return query_result.scalars().all()

    async def get_by_guid(self, guid: str) -> GoodStorage | None:
        return await self._session.get(GoodStorage, guid)

    async def get_by_good_and_specification_guid(self, good_guid: str, specification_guid: str) -> GoodStorage | None:
        query = select(GoodStorage).where(
            GoodStorage.good_guid == good_guid,
            GoodStorage.specification_guid == specification_guid,
        )
        query_result = await self._session.execute(query)

        return query_result.scalar_one_or_none()

    async def merge(self, data: GoodStorageCreateSchema) -> GoodStorage:
        good_storage = GoodStorage(**data.model_dump(exclude_unset=True))

        await self._session.merge(good_storage)
        await self._session.flush()

        return good_storage
