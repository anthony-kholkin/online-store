from sqlalchemy import insert, delete, select

from db.models.good_specification import good_specifications
from db.repositories.base import BaseDatabaseRepository


class GoodSpecificationRepository(BaseDatabaseRepository):
    async def create(self, good_guid: str, specification_guid: str):
        query = insert(good_specifications).values(good_guid=good_guid, specification_guid=specification_guid)
        await self._session.execute(query)

    async def delete(self, good_guid: str) -> None:
        query = delete(good_specifications).where(
            good_specifications.c.good_guid == good_guid,
        )
        await self._session.execute(query)

    async def check_association_with_specification(self, good_guid: str, specification_guid: str) -> bool:
        """Возвращает True, если существует связь между переданным товаром и характеристикой, иначе - False."""

        query = select(good_specifications).where(
            good_specifications.c.good_guid == good_guid,
            good_specifications.c.specification_guid == specification_guid,
        )

        return bool(await self._session.execute(query))
