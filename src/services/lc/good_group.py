from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import good_group_not_found_exception
from db.models import GoodGroup
from db.repositories.good_group import GoodGroupRepository
from db.session import get_session
from schemas.good_group import GoodGroupSchema


class GoodGroupService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        good_group_repository: GoodGroupRepository = Depends(),
    ):
        self._session = session
        self._good_group_repository = good_group_repository

    async def get_all(self) -> Sequence[GoodGroup]:
        return await self._good_group_repository.get_all()

    async def get_by_guid(self, guid: str) -> GoodGroup:
        good_group = await self._good_group_repository.get_by_guid(guid=guid)

        if not good_group:
            raise good_group_not_found_exception

        return good_group

    async def create(self, data: GoodGroupSchema) -> GoodGroup:
        good_group = await self._good_group_repository.create(data=data)

        return good_group

    async def update(self, guid: str, data: GoodGroupSchema) -> GoodGroup:
        good_group = await self.get_by_guid(guid=guid)

        await self._good_group_repository.update(instance=good_group, data=data)
        await self._session.commit()

        return good_group

    async def create_or_update(self, data: GoodGroupSchema) -> GoodGroup:
        if data.parent_group_guid:
            await self.get_by_guid(guid=data.parent_group_guid)

        good_group = await self._good_group_repository.get_by_guid(guid=data.guid)

        if not good_group:
            good_group = await self.create(data=data)
        else:
            good_group = await self.update(guid=data.guid, data=data)

        await self._session.commit()

        return good_group

    async def delete(self, guid: str) -> None:
        await self.get_by_guid(guid=guid)

        await self._good_group_repository.delete(guid=guid)
        await self._session.commit()
