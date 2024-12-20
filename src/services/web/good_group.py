import re
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

    @staticmethod
    def __remove_numbering(row: str) -> str:
        pattern = r"^\d+\.\s*"
        if re.match(pattern, row):
            return re.sub(pattern, "", row)
        else:
            return row

    def build_group_tree(
        self,
        good_groups: Sequence[Row[tuple[Any, ...] | Any]],
        parent_guid: str | None = None,
    ) -> list[GetTreeGoodGroupSchema]:
        grouped = []
        for group in good_groups:
            if group[2] == parent_guid:
                name = self.__remove_numbering(group[1])

                grouped.append(
                    GetTreeGoodGroupSchema(
                        guid=group[0],
                        name=name,
                        parent_group_guid=group[2],
                        child_groups=[],
                    )
                )

        for group in grouped:
            group.child_groups = self.build_group_tree(good_groups, parent_guid=group.guid)

        return grouped

    @lru_cache(maxsize=256)
    async def get_available_good_groups(self) -> list[GetTreeGoodGroupSchema]:
        good_groups = await self._good_group_repository.get_available_good_groups()

        return self.build_group_tree(good_groups)
