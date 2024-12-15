from typing import Sequence, Any

from sqlalchemy import select, func, Row
from sqlalchemy.orm import selectinload

from core.enum import OrderStatusEnum
from db.models import Order, Good
from db.models.order_good import order_goods
from db.repositories.base import BaseDatabaseRepository
from schemas.order import CreateOrderSchema


class OrderRepository(BaseDatabaseRepository):
    async def create(self, data: CreateOrderSchema) -> Order:
        order = Order(**data.model_dump())
        self._session.add(order)
        await self._session.flush()

        return order

    async def get_order_with_goods(self, id: int):
        query = select(Order).options(selectinload(Order.goods)).where(Order.id == id)
        result = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def get_order_goods(self, order_id: int) -> Sequence[Row[tuple[str, str, int, float]]]:
        """
        Получает товары заказа с их количеством и ценой.
        """
        query = (
            select(
                Good.name,
                Good.image_key,
                order_goods.c.quantity,
                order_goods.c.price,
            )
            .join(order_goods, Good.guid == order_goods.c.good_guid)
            .where(order_goods.c.order_id == order_id)
        )
        result = await self._session.execute(query)
        return result.fetchall()

    async def get_order_totals(self, id: int):
        """
        Подсчитывает общую стоимость и количество товаров в заказе.
        """
        query = select(
            func.sum(order_goods.c.price * order_goods.c.quantity).label("total_cost"),
            func.sum(order_goods.c.quantity).label("total_quantity"),
        ).where(order_goods.c.order_id == id)
        result = await self._session.execute(query)
        totals = result.first()

        return {
            "total_cost": totals.total_cost or 0,
            "total_quantity": totals.total_quantity or 0,
        }

    async def get_orders_by_cart_outlet_guid(
        self,
        cart_outlet_guid: str,
        page: int,
        size: int,
    ) -> tuple[Sequence[Row[tuple[Any, ...]]], int]:
        query = (
            select(
                Order.id,
                Order.guid,
                Order.status,
                Order.created_at,
                func.sum(order_goods.c.price * order_goods.c.quantity).label("total_cost"),
            )
            .join(order_goods, Order.id == order_goods.c.order_id)
            .where(Order.cart_outlet_guid == cart_outlet_guid)
            .group_by(Order.id)
        )

        count = await self.get_total_count(query=query)
        query = self.get_pagination_query(query=query, offset=(page - 1) * size, limit=size)
        query_result = await self._session.execute(query)

        return query_result.fetchall(), count

    async def get_order_by_guid(self, guid: str) -> Order | None:
        query = select(Order).where(Order.guid == guid)
        query_result = await self._session.execute(query)

        return query_result.scalar_one_or_none()

    async def update_order_status(self, instance: Order, status: OrderStatusEnum) -> None:
        instance.status = status
        await self._session.flush()
