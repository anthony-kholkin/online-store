from fastapi import APIRouter, status, Depends, Path, Body

from db.models import Order
from schemas.order import GetOrderAfterCreateSchema, UpdateOrderStatusSchema
from services.auth import authenticate
from services.web.order import OrderService

router = APIRouter(prefix="/outlets", tags=["Заказы"])


@router.patch(
    "/{cart_outlet_guid}/orders",
    status_code=status.HTTP_200_OK,
    response_model=GetOrderAfterCreateSchema,
    dependencies=[Depends(authenticate)],
)
async def update_order_status(
    cart_outlet_guid: str = Path(...),
    data: UpdateOrderStatusSchema = Body(...),
    order_service: OrderService = Depends(),
) -> Order:
    return await order_service.update_order_status(cart_outlet_guid=cart_outlet_guid, data=data)
