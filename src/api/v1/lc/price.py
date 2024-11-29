from fastapi import APIRouter, status, Depends

from db.models import Price
from schemas.price import PriceSchema
from services.lc.price import PriceService

router = APIRouter(prefix="/prices", tags=["1C Цены номенклатуры"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=PriceSchema)
async def create_or_update_price(
    data: PriceSchema,
    price_service: PriceService = Depends(),
) -> Price:
    return await price_service.create_or_update(data=data)
