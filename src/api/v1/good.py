from fastapi import APIRouter, status, Depends, Query, Security

from core.constants import RETAIL_PRICE_TYPE
from schemas.good import (
    GoodPageSchema,
    GoodWithPropertiesGetSchema,
)
from services.auth import verify_token_goods
from services.web.good import GoodService

router = APIRouter(prefix="/goods", tags=["Товары"])


@router.get("", status_code=status.HTTP_200_OK, dependencies=[Security(verify_token_goods)])
async def get_goods_by_filter(
    good_service: GoodService = Depends(),
    price_type_guid: str = Query(default=RETAIL_PRICE_TYPE),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=20),
    in_stock: bool | None = Query(default=None),
    name: str | None = Query(default=None),
) -> GoodPageSchema:
    return await good_service.get_by_filters(
        price_type_guid=price_type_guid,
        page=page,
        size=size,
        in_stock=in_stock,
        name=name,
    )


@router.get(
    "/{guid}",
    status_code=status.HTTP_200_OK,
    response_model=GoodWithPropertiesGetSchema,
    dependencies=[Security(verify_token_goods)],
)
async def get_good_by_id(
    guid: str,
    price_type_guid: str = Query(default=RETAIL_PRICE_TYPE),
    good_service: GoodService = Depends(),
) -> GoodWithPropertiesGetSchema:
    return await good_service.get_by_guid_with_properties(guid=guid, price_type_guid=price_type_guid)
