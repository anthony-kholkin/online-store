from sqlalchemy import insert

from db.models.order_good import order_goods
from db.repositories.base import BaseDatabaseRepository
from schemas.order import CreateOrderGoodDbSchema


class OrderGoodRepository(BaseDatabaseRepository):
    async def create(self, data: CreateOrderGoodDbSchema) -> None:
        query = insert(order_goods).values(**data.model_dump())
        await self._session.execute(query)

    async def bulk_create(self, data_list: list[CreateOrderGoodDbSchema]) -> None:
        values = [data.model_dump() for data in data_list]
        query = insert(order_goods).values(values)

        await self._session.execute(query)
