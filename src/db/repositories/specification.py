from typing import Sequence

from sqlalchemy import select

from db.models import Specification, Good
from db.models.good_specification import good_specifications
from db.repositories.base import BaseDatabaseRepository
from schemas.specification import (
    SpecificationSchema,
)


class SpecificationRepository(BaseDatabaseRepository):
    async def get_by_good_guid(self, good_guid: str) -> Sequence[Specification]:
        query = (
            select(Specification)
            .join(
                good_specifications,
                Specification.guid == good_specifications.c.specification_guid,
            )
            .join(Good, Good.guid == good_specifications.c.good_guid)
            .where(Good.guid == good_guid)
        )

        query_result = await self._session.execute(query)

        return query_result.scalars().all()

    async def get_by_guid(self, guid: str) -> Specification | None:
        return await self._session.get(Specification, guid)

    async def merge_batch(self, data: list[SpecificationSchema]) -> list[Specification]:
        created_specifications: list[Specification] = []

        for item in data:
            specification = Specification(**item.model_dump())
            await self._session.merge(specification)

            created_specifications.append(specification)

        await self._session.flush()

        return created_specifications

    async def create_batch(self, data: list[SpecificationSchema]) -> list[Specification]:
        specifications = [Specification(**item.model_dump()) for item in data]

        self._session.add_all(specifications)
        await self._session.flush()

        return specifications
