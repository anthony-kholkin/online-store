from sqlalchemy import insert, delete, select, RowMapping

from db.models.favorites_good import favorites_goods
from db.repositories.base import BaseDatabaseRepository


class FavoritesGoodRepository(BaseDatabaseRepository):
    async def create(self, cart_outlet_guid: str, good_guid: str):
        query = insert(favorites_goods).values(cart_outlet_guid=cart_outlet_guid, good_guid=good_guid)
        await self._session.execute(query)

    async def delete_good(self, cart_outlet_guid: str, good_guid: str) -> None:
        query = delete(favorites_goods).where(
            favorites_goods.c.cart_outlet_guid == cart_outlet_guid,
            favorites_goods.c.good_guid == good_guid,
        )
        await self._session.execute(query)

    async def get_by_guid(self, cart_outlet_guid: str, good_guid: str) -> RowMapping | None:
        query = select(favorites_goods).where(
            favorites_goods.c.cart_outlet_guid == cart_outlet_guid,
            favorites_goods.c.good_guid == good_guid,
        )

        result = await self._session.execute(query)
        row = result.fetchone()

        return row._mapping if row else None
