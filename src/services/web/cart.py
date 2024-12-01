from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    no_good_exception,
    good_not_found_exception,
    no_cart_goods_exception,
    good_in_good_not_found_exception,
)
from db.models import Cart
from db.repositories.cart import CartRepository
from db.repositories.cart_good import CartGoodRepository
from db.session import get_session
from schemas.cart import (
    AddOrUpdateGoodToCartSchema,
    GetCartSchema,
    CartGoodSchema,
    GetCartGoodSchema,
    DeleteGoodSchema,
    LightCartGoodSchema,
)
from schemas.outlet import OutletSchema
from services.lc.price_type import PriceTypeService
from services.lc.specification import SpecificationService
from services.web.good import GoodService
from storages.s3 import S3Storage


class CartService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        storage: S3Storage = Depends(),
        cart_repository: CartRepository = Depends(),
        cart_good_repository: CartGoodRepository = Depends(),
        good_service: GoodService = Depends(),
        price_type_service: PriceTypeService = Depends(),
        specification_service: SpecificationService = Depends(),
    ):
        self._session = session
        self._s3_storage = storage

        self._cart_repository = cart_repository
        self._cart_good_repository = cart_good_repository
        self._good_service = good_service
        self._price_type_service = price_type_service
        self._specification_service = specification_service

    async def add_good(
        self, cart_outlet_guid: str, data: AddOrUpdateGoodToCartSchema, outlets: list[OutletSchema]
    ) -> Cart:
        good = await self._good_service.get_by_guid(guid=data.good_guid)
        await self._specification_service.get_by_guid(guid=data.specification_guid)

        await self._good_service.check_association_with_specification(
            good_guid=data.good_guid, specification_guid=data.specification_guid
        )

        await self._price_type_service.get_by_guid(guid=data.price_type_guid)

        if not good:
            raise good_not_found_exception

        if not good.storages:
            raise no_good_exception

        for storage in good.storages:
            if storage.specification_guid == data.specification_guid and storage.in_stock < data.quantity:
                raise no_good_exception

        cart = await self._cart_repository.get_cart_by_cart_outlet_guid(cart_outlet_guid=cart_outlet_guid)

        if not cart:
            cart = await self._cart_repository.create(cart_outlet_guid=cart_outlet_guid)

        data_to_create = CartGoodSchema(cart_outlet_guid=cart.cart_outlet_guid, **data.model_dump())

        await self._cart_good_repository.create(data=data_to_create)
        await self._session.commit()

        return cart

    async def delete_good(self, cart_outlet_guid: str, good_guid: str, specification_guid: str) -> DeleteGoodSchema:
        cart_good = await self._cart_good_repository.get_by_guid(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
        )

        if not cart_good:
            raise good_in_good_not_found_exception

        await self._cart_good_repository.delete_good(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
        )
        await self._session.commit()

        return DeleteGoodSchema(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
        )

    async def update_good_count_in_cart(
        self, cart_outlet_guid: str, data: AddOrUpdateGoodToCartSchema
    ) -> CartGoodSchema:
        good = await self._good_service.get_by_guid(guid=data.good_guid)
        await self._specification_service.get_by_guid(guid=data.specification_guid)

        await self._good_service.check_association_with_specification(
            good_guid=data.good_guid, specification_guid=data.specification_guid
        )

        await self._price_type_service.get_by_guid(guid=data.price_type_guid)

        if not good:
            raise good_not_found_exception

        if not good.storages:
            raise no_good_exception

        for storage in good.storages:
            if storage.specification_guid == data.specification_guid and storage.in_stock < data.quantity:
                raise no_good_exception

        cart_good = await self._cart_repository.get_cart_by_cart_outlet_guid_with_cart_goods(
            cart_outlet_guid=cart_outlet_guid
        )

        if not cart_good:
            raise no_cart_goods_exception

        await self._cart_good_repository.update_quantity(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=data.good_guid,
            specification_guid=data.specification_guid,
            quantity=data.quantity,
        )
        await self._session.commit()

        return CartGoodSchema(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=data.good_guid,
            specification_guid=data.specification_guid,
            price_type_guid=data.price_type_guid,
            quantity=data.quantity,
        )

    async def get_cart(self, cart_outlet_guid: str) -> GetCartSchema:
        cart_rows = await self._cart_repository.get_cart_with_prices(cart_outlet_guid=cart_outlet_guid)

        if not cart_rows:
            return GetCartSchema(cart_outlet_guid=cart_outlet_guid, goods=[], total_cost=0)

        total_cost = 0

        goods: list[GetCartGoodSchema] = []

        for row in cart_rows:
            image_key = row.image_key

            if image_key is None:
                image_key = await self._s3_storage.generate_presigned_url(key="image not found.png")

            goods.append(
                GetCartGoodSchema(
                    guid=row.guid,
                    specification_guid=row.specification_guid,
                    price_type_guid=row.price_type_guid,
                    name=row.name,
                    image_key=image_key,
                    is_favorite=False,
                    quantity=row.quantity,
                    price=row.price,
                )
            )

            total_cost += row.price * row.quantity

        return GetCartSchema(cart_outlet_guid=cart_outlet_guid, goods=goods, total_cost=total_cost)

    async def get_good_quantity_in_cart(
        self, cart_outlet_guid: str, good_guid: str, specification_guid: str
    ) -> LightCartGoodSchema:
        cart_good = await self._cart_good_repository.get_by_guid(
            cart_outlet_guid=cart_outlet_guid, good_guid=good_guid, specification_guid=specification_guid
        )

        return LightCartGoodSchema(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
            specification_guid=specification_guid,
            quantity=cart_good.quantity if cart_good else 0,
        )
