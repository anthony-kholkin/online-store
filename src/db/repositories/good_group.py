from typing import Sequence


from sqlalchemy import delete, select, exists, or_, and_
from sqlalchemy.orm import aliased

from db.models import GoodGroup, Good, GoodStorage, Price
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

    # async def get_good_groups_by_pattern_name(self, pattern: str = r"^\d+\.\s.*$") -> Sequence[GoodGroup]:
    #     query = select(GoodGroup).where(GoodGroup.name.op("~")(pattern)).order_by(GoodGroup.name)
    #     query_result = await self._session.execute(query)
    #
    #     return query_result.scalars().all()

    async def get_available_good_groups(self) -> Sequence[GoodGroup]:
        child_group_alias = aliased(GoodGroup)

        goods_in_group_with_stock = (
            select(Good.guid)
            .join(GoodStorage, Good.guid == GoodStorage.good_guid)
            .where(and_(GoodStorage.in_stock > 0, Good.good_group_guid == GoodGroup.guid))
            .exists()
        )

        child_groups_with_stock = (
            select(child_group_alias.guid)
            .where(child_group_alias.parent_group_guid == GoodGroup.guid)
            .where(
                exists(
                    select(1)
                    .select_from(Good)
                    .join(GoodStorage, Good.guid == GoodStorage.good_guid)
                    .where(
                        and_(
                            GoodStorage.in_stock > 0,
                            Good.good_group_guid == child_group_alias.guid,
                        )
                    )
                )
            )
            .exists()
        )

        query = select(GoodGroup).where(or_(goods_in_group_with_stock, child_groups_with_stock))

        result = await self._session.execute(query)
        return result.scalars().all()
