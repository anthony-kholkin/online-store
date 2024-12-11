from fastapi import APIRouter, status, Depends

from db.models import Good
from schemas.good import (
    GoodWithSpecsGetSchema,
    GoodWithSpecsCreateSchema,
    ImageAddSchema,
)
from services.auth import authenticate
from services.lc.good import lCGoodService

router = APIRouter(prefix="/goods", tags=["1C Номенклатура"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=GoodWithSpecsGetSchema, dependencies=[Depends(authenticate)]
)
async def create_good(
    data: GoodWithSpecsCreateSchema,
    good_service: lCGoodService = Depends(),
) -> Good:
    return await good_service.merge(data=data)


@router.post("/image", status_code=status.HTTP_201_CREATED, dependencies=[Depends(authenticate)])
async def add_image(
    data: ImageAddSchema,
    good_service: lCGoodService = Depends(),
) -> str:
    return await good_service.add_image(data=data)
