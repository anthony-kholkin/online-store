from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import PROPERTY_COLUMNS
from core.exceptions import (
    good_not_found_exception,
    no_goods_specs_associations_exception,
)
from db.repositories.good import GoodRepository
from db.repositories.good_specification import GoodSpecificationRepository
from db.session import get_session
from schemas.good import (
    GoodCardGetSchema,
    GoodPageSchema,
    GoodWithPropertiesGetSchema,
    GoodPropertyGetSchema,
)
from schemas.good_storage import GoodStorageGetSchema
from schemas.price import PriceGetSchema
from schemas.specification import SpecificationSchema
from services.base.good import BaseGoodService
from services.lc.good_group import GoodGroupService
from services.lc.specification import SpecificationService

from storages.s3 import S3Storage


class GoodService(BaseGoodService):
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        storage: S3Storage = Depends(),
        good_repository: GoodRepository = Depends(),
        good_specification_repository: GoodSpecificationRepository = Depends(),
        specification_service: SpecificationService = Depends(),
        good_group_service: GoodGroupService = Depends(),
    ):
        super().__init__(good_repository)
        self._session = session
        self._s3_storage = storage

        self._specification_service = specification_service
        self._good_specification_repository = good_specification_repository
        self._good_group_service = good_group_service

    async def get_by_guid_with_properties(self, guid: str, price_type_guid: str) -> GoodWithPropertiesGetSchema:
        good = await self._good_repository.get_by_guid(guid=guid)

        if not good:
            raise good_not_found_exception

        image_key = await self._s3_storage.generate_presigned_url(key=good.image_key)

        if image_key is None:
            image_key = await self._s3_storage.generate_presigned_url(key="image not found.png")

        property_schemas = [
            GoodPropertyGetSchema(name=value, value=getattr(good, name))
            for name, value in PROPERTY_COLUMNS.items()
            if getattr(good, name)
        ]

        storages: list[GoodStorageGetSchema] = []

        for storage in good.storages:
            storages.append(
                GoodStorageGetSchema(
                    good_guid=good.guid,
                    specification_guid=storage.specification_guid,
                    in_stock=storage.in_stock,
                    specification_name=storage.specification.name,
                )
            )

        prices = [
            PriceGetSchema(
                good_guid=price.good_guid,
                specification=SpecificationSchema(
                    guid=price.specification_guid,
                    name=price.specification.name,
                ),
                price_type=price.price_type,
                value=price.value,
            )
            for price in good.prices
            if price.price_type_guid == price_type_guid
        ]

        return GoodWithPropertiesGetSchema(
            guid=good.guid,
            name=good.name,
            good_group_guid=good.good_group_guid,
            description=good.description,
            type=good.type,
            image_key=image_key,
            properties=property_schemas,
            storages=storages,
            prices=prices,
        )

    async def get_by_filters(
        self,
        price_type_guid: str,
        price_from: float | None,
        price_to: float | None,
        page: int,
        size: int,
        in_stock: bool | None = None,
        name: str | None = None,
    ) -> GoodPageSchema:
        pagination_goods, total = await self._good_repository.get_by_filters(
            price_type_guid=price_type_guid,
            price_from=price_from,
            price_to=price_to,
            page=page,
            size=size,
            in_stock=in_stock,
            name=name,
        )

        pagination_result = self.get_pagination_result(objects=pagination_goods, page=page, size=size, total=total)

        schema_goods = []

        for good in pagination_result["items"]:
            image_key = await self._s3_storage.generate_presigned_url(key=good.image_key)
            good_schema = GoodCardGetSchema.model_validate(good)
            good_schema.image_key = image_key
            good_schema.prices = [
                PriceGetSchema(
                    good_guid=price.good_guid,
                    specification=SpecificationSchema(
                        guid=price.specification_guid,
                        name=price.specification.name,
                    ),
                    price_type=price.price_type,
                    value=price.value,
                )
                for price in good.prices
                if price.price_type_guid == price_type_guid
            ]

            if good_schema.image_key is None:
                good_schema.image_key = await self._s3_storage.generate_presigned_url(key="image not found.png")

            schema_goods.append(good_schema)

        return GoodPageSchema(
            items=schema_goods,
            page=pagination_result["page"],
            size=pagination_result["size"],
            pages=pagination_result["pages"],
            total=pagination_result["total"],
        )

    async def check_association_with_specification(self, good_guid: str, specification_guid: str) -> None:
        is_association = await self._good_specification_repository.check_association_with_specification(
            good_guid=good_guid, specification_guid=specification_guid
        )

        if not is_association:
            raise no_goods_specs_associations_exception
