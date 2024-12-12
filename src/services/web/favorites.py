from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import (
    good_not_found_exception,
)
from db.repositories.favorites import FavoritesRepository
from db.repositories.favorites_good import FavoritesGoodRepository
from db.session import get_session
from schemas.favorites import GetFavoritesGoodSchema, GetFavoritesSchema, AddOrDeleteFavoritesSchema
from services.web.good import GoodService
from storages.s3 import S3Storage


class FavoritesService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        storage: S3Storage = Depends(),
        favorites_repository: FavoritesRepository = Depends(),
        favorites_good_repository: FavoritesGoodRepository = Depends(),
        good_service: GoodService = Depends(),
    ):
        self._session = session
        self._s3_storage = storage

        self._favorites_repository = favorites_repository
        self._favorites_good_repository = favorites_good_repository
        self._good_service = good_service

    async def add_good(self, cart_outlet_guid: str, good_guid: str) -> AddOrDeleteFavoritesSchema:
        good = await self._good_service.get_by_guid(guid=good_guid)

        if not good:
            raise good_not_found_exception

        favorites = await self._favorites_repository.get_cart_by_cart_outlet_guid(cart_outlet_guid=cart_outlet_guid)

        if not favorites:
            favorites = await self._favorites_repository.create(cart_outlet_guid=cart_outlet_guid)

        favorites_good = await self._favorites_good_repository.get_by_guid(
            cart_outlet_guid=cart_outlet_guid, good_guid=good_guid
        )

        if not favorites_good:
            await self._favorites_good_repository.create(cart_outlet_guid=cart_outlet_guid, good_guid=good_guid)
            await self._session.commit()

        return AddOrDeleteFavoritesSchema(cart_outlet_guid=favorites.cart_outlet_guid, good_guid=good.guid)

    async def get_favorites(self, cart_outlet_guid: str, price_type_guid: str) -> GetFavoritesSchema:
        favorites_rows = await self._favorites_repository.get_favorites_with_prices(
            cart_outlet_guid=cart_outlet_guid, price_type_guid=price_type_guid
        )

        if not favorites_rows:
            return GetFavoritesSchema(
                cart_outlet_guid=cart_outlet_guid,
                goods=[],
            )

        goods = []

        for row in favorites_rows:
            image_key = row.image_key

            if image_key is None:
                image_key = await self._s3_storage.generate_presigned_url(key="image not found.png")

            goods.append(
                GetFavoritesGoodSchema(
                    guid=row.good_guid,
                    name=row.name,
                    image_key=image_key,
                    price=row.price,
                )
            )

        return GetFavoritesSchema(
            cart_outlet_guid=cart_outlet_guid,
            goods=goods,
        )

    async def delete_good(self, cart_outlet_guid: str, good_guid: str) -> AddOrDeleteFavoritesSchema:
        cart_good = await self._favorites_good_repository.get_by_guid(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
        )

        if cart_good:
            await self._favorites_good_repository.delete_good(cart_outlet_guid=cart_outlet_guid, good_guid=good_guid)
            await self._session.commit()

        return AddOrDeleteFavoritesSchema(
            cart_outlet_guid=cart_outlet_guid,
            good_guid=good_guid,
        )
