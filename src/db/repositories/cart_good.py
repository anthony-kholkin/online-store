from sqlalchemy import insert, delete, select, RowMapping, update

from db.models.cart_good import cart_goods
from db.repositories.base import BaseDatabaseRepository
from schemas.cart import CartGoodSchema


class CartGoodRepository(BaseDatabaseRepository):
    async def create(self, data: CartGoodSchema):
        query = insert(cart_goods).values(**data.model_dump())
        await self._session.execute(query)

    async def delete_good(self, cart_outlet_guid: str, good_guid: str, specification_guid: str) -> None:
        query = delete(cart_goods).where(
            cart_goods.c.cart_outlet_guid == cart_outlet_guid,
            cart_goods.c.good_guid == good_guid,
            cart_goods.c.specification_guid == specification_guid,
        )
        await self._session.execute(query)

    async def get_by_guid(self, cart_outlet_guid: str, good_guid: str, specification_guid: str) -> RowMapping | None:
        query = select(cart_goods).where(
            cart_goods.c.cart_outlet_guid == cart_outlet_guid,
            cart_goods.c.good_guid == good_guid,
            cart_goods.c.specification_guid == specification_guid,
        )

        result = await self._session.execute(query)
        row = result.fetchone()

        return row._mapping if row else None

    async def update_quantity(
        self, cart_outlet_guid: str, good_guid: str, specification_guid: str, quantity: int
    ) -> None:
        query = (
            update(cart_goods)
            .where(
                cart_goods.c.cart_outlet_guid == cart_outlet_guid,
                cart_goods.c.good_guid == good_guid,
                cart_goods.c.specification_guid == specification_guid,
            )
            .values(quantity=quantity)
        )
        await self._session.execute(query)
