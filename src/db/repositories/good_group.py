from typing import Sequence


from sqlalchemy import delete, select

from db.models import GoodGroup
from db.repositories.base import BaseDatabaseRepository
from schemas.good_group import GoodGroupSchema


class GoodGroupRepository(BaseDatabaseRepository):
    async def create(self, data: GoodGroupSchema) -> GoodGroup:
        good_group = GoodGroup()

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(good_group, key, value)

        self._session.add(good_group)
        await self._session.flush()

        return good_group

    async def get_all(self) -> Sequence[GoodGroup]:
        query_result = await self._session.execute(select(GoodGroup))

        return query_result.scalars().all()

    async def get_by_guid(self, guid: str) -> GoodGroup | None:
        return await self._session.get(GoodGroup, guid)

    async def update(self, instance: GoodGroup, data: GoodGroupSchema) -> None:
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(instance, key, value)

        await self._session.flush()

    async def delete(self, guid: str) -> None:
        await self._session.execute(delete(GoodGroup).where(GoodGroup.guid == guid))

    async def get_good_groups_by_pattern_name(self, pattern: str = r"^\d+\.\s.*$") -> Sequence[GoodGroup]:
        query = select(GoodGroup).where(GoodGroup.name.op("~")(pattern)).order_by(GoodGroup.name)
        query_result = await self._session.execute(query)

        return query_result.scalars().all()
