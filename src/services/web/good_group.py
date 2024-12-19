from functools import lru_cache
from typing import Sequence

from fastapi import Depends

from db.models import GoodGroup
from db.repositories.good_group import GoodGroupRepository
from schemas.good_group import GetTreeGoodGroupSchema


class GoodGroupService:
    def __init__(
        self,
        good_group_repository: GoodGroupRepository = Depends(),
    ):
        self._good_group_repository = good_group_repository

    def build_group_tree(
        self,
        good_groups: Sequence[GoodGroup],
        parent_guid: str | None = None,
    ) -> list[GetTreeGoodGroupSchema]:
        grouped = [
            GetTreeGoodGroupSchema(
                guid=group.guid,
                name=group.name,
                parent_group_guid=group.parent_group_guid,
                child_groups=[],
            )
            for group in good_groups
            if group.parent_group_guid == parent_guid
        ]

        for group in grouped:
            group.child_groups = self.build_group_tree(good_groups, parent_guid=group.guid)

        return grouped

    @lru_cache(maxsize=256)
    async def get_available_good_groups(self, price_type_guid: str) -> list[GetTreeGoodGroupSchema]:
        good_groups = await self._good_group_repository.get_available_good_groups(price_type_guid=price_type_guid)

        return self.build_group_tree(good_groups)
