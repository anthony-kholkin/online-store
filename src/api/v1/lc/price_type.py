from typing import Sequence

from fastapi import APIRouter, status, Depends


from db.models.price_type import PriceType
from schemas.price_type import PriceTypeSchema
from services.auth import authenticate
from services.lc.price_type import PriceTypeService

router = APIRouter(prefix="/price-types", tags=["1C Виды цен номенклатуры"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=PriceTypeSchema, dependencies=[Depends(authenticate)]
)
async def create_price_type(
    data: PriceTypeSchema,
    price_type_service: PriceTypeService = Depends(),
) -> PriceType:
    return await price_type_service.create_or_update(data=data)


@router.get(
    "", status_code=status.HTTP_200_OK, response_model=list[PriceTypeSchema], dependencies=[Depends(authenticate)]
)
async def get_price_types(
    price_type_service: PriceTypeService = Depends(),
) -> Sequence[PriceType]:
    return await price_type_service.get_all()


@router.get(
    "/{guid}", status_code=status.HTTP_200_OK, response_model=PriceTypeSchema, dependencies=[Depends(authenticate)]
)
async def get_price_type_by_id(
    guid: str,
    price_type_service: PriceTypeService = Depends(),
) -> PriceType:
    return await price_type_service.get_by_guid(guid=guid)
