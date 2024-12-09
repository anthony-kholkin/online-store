import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import no_order_exception, access_denied_exception
from db.models import Order
from db.repositories.order import OrderRepository
from db.repositories.order_good import OrderGoodRepository
from db.session import get_session
from schemas.order import (
    CreateOrderWithGoodsSchema,
    CreateOrderSchema,
    CreateOrderGoodDbSchema,
    GetOrderWithGoodsSchema,
    GetOrderGoodSchema,
    GetOrderList,
)

from services.web.good import GoodService
from storages.s3 import S3Storage


class OrderService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        storage: S3Storage = Depends(),
        order_repository: OrderRepository = Depends(),
        order_good_repository: OrderGoodRepository = Depends(),
        good_service: GoodService = Depends(),
    ):
        self._session = session
        self._s3_storage = storage

        self._order_repository = order_repository
        self._order_good_repository = order_good_repository
        self._good_service = good_service

    async def create(self, data: CreateOrderWithGoodsSchema, cart_outlet_guid: str) -> Order:
        for good_data in data.goods:
            await self._good_service.get_by_guid_with_check_storages(
                good_guid=good_data.good_guid,
                specification_guid=good_data.specification_guid,
                good_quantity=good_data.quantity,
            )

        order = await self._order_repository.create(
            data=CreateOrderSchema(
                guid=datetime.datetime.now().isoformat(),
                cart_outlet_guid=cart_outlet_guid,
            )
        )

        await self._order_good_repository.bulk_create(
            data_list=[CreateOrderGoodDbSchema(order_id=order.id, **good_data.model_dump()) for good_data in data.goods]
        )
        await self._session.commit()

        return order

    async def get_by_id(self, id: int, cart_outlet_guid: str) -> GetOrderWithGoodsSchema:
        order = await self._order_repository.get_order_with_goods(id)

        if not order:
            raise no_order_exception

        if order.cart_outlet_guid != cart_outlet_guid:
            raise access_denied_exception

        order_goods = await self._order_repository.get_order_goods(order_id=id)
        totals = await self._order_repository.get_order_totals(id)

        goods = []

        for good in order_goods:
            image_key = good.image_key

            if image_key is None:
                image_key = await self._s3_storage.generate_presigned_url(key="image not found.png")

            goods.append(
                GetOrderGoodSchema(
                    name=good.name,
                    image_key=image_key,
                    quantity=good.quantity,
                    price=good.price,
                )
            )

        return GetOrderWithGoodsSchema(
            id=order.id,
            guid=order.guid,
            cart_outlet_guid=order.cart_outlet_guid,
            status=order.status,
            total_cost=totals["total_cost"],
            total_quantity=totals["total_quantity"],
            created_at=order.created_at,
            goods=goods,
        )

    async def get_all_by_cart_outlet_guid(self, cart_outlet_guid: str) -> list[GetOrderList]:
        orders = await self._order_repository.get_orders_by_cart_outlet_guid(cart_outlet_guid)

        return [
            GetOrderList(
                id=order.id,
                guid=order.guid,
                status=order.status,
                created_at=order.created_at,
                total_cost=order.total_cost or 0,
            )
            for order in orders
        ]
