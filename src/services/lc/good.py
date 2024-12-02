from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import encoded_image_exception, upload_image_exception
from db.models import Good
from db.repositories.good import GoodRepository
from db.repositories.good_specification import GoodSpecificationRepository
from db.session import get_session
from schemas.good import (
    GoodWithSpecsCreateSchema,
    GoodCreateSchema,
    ImageAddSchema,
)
from services.base.good import BaseGoodService
from services.lc.good_group import GoodGroupService
from services.lc.specification import SpecificationService
from services.utils import resize_image, base64_to_bytes_image
from storages.s3 import S3Storage


class lCGoodService(BaseGoodService):
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

        self._good_specification_repository = good_specification_repository

        self._specification_service = specification_service
        self._good_group_service = good_group_service

    async def merge(self, data: GoodWithSpecsCreateSchema) -> Good:
        """Создать или обновить товар со связанными характеристиками."""

        await self._good_group_service.get_by_guid(guid=data.good_group_guid)

        good = await self._good_repository.merge(data=GoodCreateSchema(**data.model_dump(exclude={"specifications"})))

        await self._good_specification_repository.delete(good_guid=data.guid)
        specifications = await self._specification_service.merge_batch(data=data.specifications)

        for specification in specifications:
            await self._good_specification_repository.create(good_guid=good.guid, specification_guid=specification.guid)
            good.specifications.append(specification)

        await self._session.commit()

        return good

    async def add_image(self, data: ImageAddSchema) -> str:
        good = await self.get_by_guid(guid=data.good_guid)

        image = base64_to_bytes_image(base64_image=data.image)

        if not image:
            raise encoded_image_exception

        image_key = await self._s3_storage.upload_file(
            key=data.good_guid,
            data=resize_image(image=image),
            content_type="image/jpeg",
        )

        if not image_key:
            raise upload_image_exception

        await self._good_repository.add_image(instance=good, image_key=image_key)
        await self._session.commit()

        return good.guid
