from typing import Sequence, Any

from sqlalchemy import delete, select, text, Row

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

    async def get_available_good_groups(self) -> Sequence[Row[tuple[Any, ...] | Any]]:
        sql_query = text("""
        WITH RECURSIVE group_hierarchy AS (
            SELECT gg.guid group_guid,gg.name group_name,gg.parent_group_guid parent_group_guid
            FROM good_groups gg
            JOIN goods g ON gg.guid = g.good_group_guid
            JOIN good_storages gs ON g.guid = gs.good_guid
            WHERE gs.in_stock > 0
        
            UNION ALL
        
            SELECT gg.guid group_guid, gg.name group_name, gg.parent_group_guid
            FROM good_groups gg
            JOIN group_hierarchy gh ON gg.guid = gh.parent_group_guid
        )
        SELECT DISTINCT group_guid, group_name, parent_group_guid
        FROM group_hierarchy
        ORDER BY 2;
        """)

        result = await self._session.execute(sql_query)

        return result.fetchall()
