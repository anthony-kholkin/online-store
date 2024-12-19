from functools import lru_cache
from typing import Sequence, Any

from fastapi import Depends
from sqlalchemy import Row

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
        good_groups: Sequence[Row[tuple[Any, ...] | Any]],
        parent_guid: str | None = None,
    ) -> list[GetTreeGoodGroupSchema]:
        grouped = [
            GetTreeGoodGroupSchema(
                guid=group[0],
                name=group[1],
                parent_group_guid=group[2],
                child_groups=[],
            )
            for group in good_groups
            if group[2] == parent_guid
        ]

        for group in grouped:
            group.child_groups = self.build_group_tree(good_groups, parent_guid=group.guid)

        return grouped

    @lru_cache(maxsize=256)
    async def get_available_good_groups(self) -> list[GetTreeGoodGroupSchema]:
        good_groups = await self._good_group_repository.get_available_good_groups()

        return self.build_group_tree(good_groups)
