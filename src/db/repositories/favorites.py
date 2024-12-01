from typing import Sequence

from sqlalchemy import select, and_, Row, func

from db.models import Favorites, Price, Good, GoodStorage
from db.models.favorites_good import favorites_goods
from db.repositories.base import BaseDatabaseRepository


class FavoritesRepository(BaseDatabaseRepository):
    async def create(self, cart_outlet_guid: str) -> Favorites:
        favorites = Favorites(cart_outlet_guid=cart_outlet_guid)  # type: ignore
        self._session.add(favorites)
        await self._session.flush()

        return favorites

    async def get_favorites_with_prices(self, cart_outlet_guid: str, price_type_guid: str):
        query = (
            select(
                Favorites.cart_outlet_guid,
                Good.guid.label("good_guid"),
                Good.name.label("name"),
                Good.image_key.label("image_key"),
                func.min(Price.value).label("price"),
            )
            .join(favorites_goods, Favorites.cart_outlet_guid == favorites_goods.c.cart_outlet_guid)
            .join(Good, favorites_goods.c.good_guid == Good.guid)
            .join(Price, and_(
                Price.good_guid == Good.guid,
                Price.price_type_guid == price_type_guid
            ))
            .join(GoodStorage, and_(
                GoodStorage.good_guid == Good.guid,
                GoodStorage.in_stock > 0
            ))
            .where(Favorites.cart_outlet_guid == cart_outlet_guid)
            .group_by(Favorites.cart_outlet_guid, Good.guid, Good.name, Good.image_key)
        )

        result = await self._session.execute(query)
        return result.fetchall()
