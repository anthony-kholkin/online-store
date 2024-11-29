from typing import Sequence

from sqlalchemy import select, and_, Row

from db.models import Cart, Price, Good
from db.models.cart_good import cart_goods
from db.repositories.base import BaseDatabaseRepository


class CartRepository(BaseDatabaseRepository):
    async def create(self, cart_outlet_guid: str) -> Cart:
        cart = Cart(cart_outlet_guid=cart_outlet_guid)  # type: ignore
        self._session.add(cart)
        await self._session.flush()

        return cart

    async def get_cart_by_outlet_guid(self, cart_outlet_guid: str) -> Cart | None:
        query = (
            select(Cart, cart_goods)
            .join(cart_goods, Cart.cart_outlet_guid == cart_goods.c.cart_outlet_guid)
            .where(Cart.cart_outlet_guid == cart_outlet_guid)
        )

        query_result = await self._session.execute(query)
        results = query_result.fetchall()

        if not results:
            return None

        cart, *_ = results[0]

        return cart

    async def get_cart_with_prices(
        self, cart_outlet_guid: str
    ) -> Sequence[Row[tuple[str, str, str, int, str, str, str | None, float]]]:
        """
        Получить корзину с ценами для каждого товара, основываясь на good_guid, specification_guid и price_type_guid.
        """
        query = (
            select(
                Cart.cart_outlet_guid,
                cart_goods.c.specification_guid,
                cart_goods.c.price_type_guid,
                cart_goods.c.quantity,
                Good.guid.label("guid"),
                Good.name.label("name"),
                Good.image_key.label("image_key"),
                Price.value.label("price"),
            )
            .join(cart_goods, Cart.cart_outlet_guid == cart_goods.c.cart_outlet_guid)
            .join(
                Price,
                and_(
                    Price.good_guid == cart_goods.c.good_guid,
                    Price.specification_guid == cart_goods.c.specification_guid,
                    Price.price_type_guid == cart_goods.c.price_type_guid,
                ),
            )
            .join(Good, Good.guid == cart_goods.c.good_guid)
            .where(Cart.cart_outlet_guid == cart_outlet_guid)
        )

        result = await self._session.execute(query)

        return result.fetchall()
