
from fastapi import Depends

from db.repositories.good_group import GoodGroupRepository
from schemas.good_group import GetGoodGroupSchema


class GoodGroupService:
    def __init__(
        self,
        good_group_repository: GoodGroupRepository = Depends(),
    ):
        self._good_group_repository = good_group_repository

    async def get_available_good_groups(self) -> list[GetGoodGroupSchema]:
        good_groups = await self._good_group_repository.get_good_groups_by_pattern_name()

        return [
            GetGoodGroupSchema(guid=good_group.guid, name=good_group.name.split(". ")[1]) for good_group in good_groups
        ]
