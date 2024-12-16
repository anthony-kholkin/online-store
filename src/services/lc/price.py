from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Price
from db.repositories.price import PriceRepository
from db.session import get_session
from schemas.price import PriceSchema
from services.base.good import BaseGoodService
from services.lc.price_type import PriceTypeService
from services.lc.specification import SpecificationService


class PriceService:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
        price_repository: PriceRepository = Depends(),
        good_service: BaseGoodService = Depends(),
        specification_service: SpecificationService = Depends(),
        price_type_service: PriceTypeService = Depends(),
    ):
        self._session = session
        self._price_repository = price_repository
        self._good_service = good_service
        self._specification_service = specification_service
        self._price_type_service = price_type_service

    async def get_by_good_and_specification_guid(self, good_guid: str, specification_guid: str) -> Sequence[Price]:
        return await self._price_repository.get_by_good_and_specification_guid(
            good_guid=good_guid, specification_guid=specification_guid
        )

    async def create_or_update(self, data: PriceSchema) -> Price:
        await self._good_service.get_by_guid(guid=data.good_guid)
        await self._specification_service.get_by_guid(guid=data.specification_guid)
        await self._price_type_service.get_by_guid(guid=data.price_type_guid)

        price = await self._price_repository.merge(data=data)
        await self._session.commit()

        return price

    async def create_or_update_batch(self, data: list[PriceSchema]) -> list[Price]:
        prices = []

        for price_data in data:
            await self._good_service.get_by_guid(guid=price_data.good_guid)
            await self._specification_service.get_by_guid(guid=price_data.specification_guid)
            await self._price_type_service.get_by_guid(guid=price_data.price_type_guid)

            price = await self._price_repository.merge(data=price_data)
            prices.append(price)

        await self._session.commit()
        return prices
