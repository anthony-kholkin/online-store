from fastapi import APIRouter, status, Depends

from db.models import Price
from schemas.price import PriceSchema, BatchPriceSchema
from services.auth import authenticate
from services.lc.price import PriceService

router = APIRouter(prefix="/prices", tags=["1C Цены номенклатуры"])


@router.post("", status_code=status.HTTP_200_OK, response_model=PriceSchema, dependencies=[Depends(authenticate)])
async def create_or_update_price(
    data: PriceSchema,
    price_service: PriceService = Depends(),
) -> Price:
    return await price_service.create_or_update(data=data)


@router.post(
    "/batch", status_code=status.HTTP_200_OK, response_model=list[PriceSchema], dependencies=[Depends(authenticate)]
)
async def create_or_update_prices_batch(
    data: BatchPriceSchema,
    price_service: PriceService = Depends(),
) -> list[Price]:
    return await price_service.create_or_update_batch(data=data.prices)
