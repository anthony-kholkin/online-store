from fastapi import status, Depends, Path, APIRouter, Body, Security, Query

from db.models import Order
from schemas.order import (
    GetOrderWithGoodsSchema,
    CreateOrderWithGoodsSchema,
    GetOrderAfterCreateSchema,
    OrderPageSchema,
)
from services.auth import verify_token_outlets

from services.web.order import OrderService

router = APIRouter(prefix="/outlets", tags=["Заказы"])


@router.post(
    "/{cart_outlet_guid}/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderAfterCreateSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def create_order(
    cart_outlet_guid: str = Path(...),
    data: CreateOrderWithGoodsSchema = Body(...),
    order_service: OrderService = Depends(),
) -> Order:
    return await order_service.create(data=data, cart_outlet_guid=cart_outlet_guid)


@router.get(
    "/{cart_outlet_guid}/orders/{id}",
    status_code=status.HTTP_200_OK,
    response_model=GetOrderWithGoodsSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def get_order_by_id(
    cart_outlet_guid: str = Path(...),
    id: int = Path(...),
    order_service: OrderService = Depends(),
) -> GetOrderWithGoodsSchema:
    return await order_service.get_by_id(id=id, cart_outlet_guid=cart_outlet_guid)


@router.get(
    "/{cart_outlet_guid}/orders",
    status_code=status.HTTP_200_OK,
    response_model=OrderPageSchema,
    dependencies=[Security(verify_token_outlets)],
)
async def get_orders(
    cart_outlet_guid: str = Path(...),
    page: int = Query(ge=1, default=1),
    size: int = Query(ge=1, le=100, default=20),
    order_service: OrderService = Depends(),
) -> OrderPageSchema:
    return await order_service.get_all_by_cart_outlet_guid(cart_outlet_guid=cart_outlet_guid, page=page, size=size)
