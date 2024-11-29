from fastapi import APIRouter, status, Depends

from schemas.good_storage import GoodStorageCreateSchema, GoodStorageGetSchema
from services.lc.good_storage import GoodStorageService

router = APIRouter(prefix="/good_storage", tags=["1C Остатки номенклатуры"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=GoodStorageGetSchema)
async def create_or_update_good_storage(
    data: GoodStorageCreateSchema,
    good_storage_service: GoodStorageService = Depends(),
) -> GoodStorageGetSchema:
    return await good_storage_service.create_or_update(data=data)
