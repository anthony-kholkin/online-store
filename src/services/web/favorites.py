from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    cart_not_found_exception,
    no_good_exception,
    good_not_found_exception,
    no_cart_goods_exception,
    good_in_good_not_found_exception, favorites_not_found_exception,
)
from db.models import Cart
from db.repositories.cart import CartRepository
from db.repositories.cart_good import CartGoodRepository
from db.repositories.favorites import FavoritesRepository
from db.session import get_session
from schemas.favorites import GetFavoritesGoodSchema, GetFavoritesSchema
from schemas.outlet import OutletSchema
from services.lc.price_type import PriceTypeService
from services.lc.specification import SpecificationService
from services.web.good import GoodService
from storages.s3 import S3Storage


class FavoritesService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        storage: S3Storage = Depends(),
        favorites_repository: FavoritesRepository = Depends(),
        # cart_good_repository: CartGoodRepository = Depends(),
        good_service: GoodService = Depends(),
    ):
        self._session = session
        self._s3_storage = storage

        self._favorites_repository = favorites_repository
        # self._cart_good_repository = cart_good_repository
        self._good_service = good_service

    async def get_favorites(self, cart_outlet_guid: str, price_type_guid: str) -> GetFavoritesSchema:
        favorites_rows = await self._favorites_repository.get_favorites_with_prices(cart_outlet_guid=cart_outlet_guid,
                                                                                    price_type_guid=price_type_guid)

        if not favorites_rows:
            raise favorites_not_found_exception

        goods = [
            GetFavoritesGoodSchema(
                guid=row.good_guid,
                name=row.name,
                image_key=row.image_key,
                price=row.price,
            )
            for row in favorites_rows
        ]

        return GetFavoritesSchema(
            cart_outlet_guid=cart_outlet_guid,
            goods=goods,
        )


