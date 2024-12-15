from datetime import datetime

from pydantic import BaseModel

from core.enum import OrderStatusEnum
from schemas.base import BaseOrmSchema


class CreateOrderSchema(BaseOrmSchema):
    guid: str
    cart_outlet_guid: str
    status: OrderStatusEnum = OrderStatusEnum.OPEN


class GetOrderAfterCreateSchema(CreateOrderSchema):
    id: int


class CreateOrderGoodSchema(BaseModel):
    good_guid: str
    specification_guid: str
    quantity: int
    price: float


class CreateOrderGoodDbSchema(BaseOrmSchema, CreateOrderGoodSchema):
    order_id: int


class CreateOrderWithGoodsSchema(BaseOrmSchema):
    goods: list[CreateOrderGoodSchema]


class GetOrderGoodSchema(BaseModel):
    name: str
    image_key: str
    quantity: int
    price: float


class GetOrderWithGoodsSchema(BaseOrmSchema):
    id: int
    guid: str
    cart_outlet_guid: str
    status: OrderStatusEnum
    total_cost: float
    total_quantity: int
    created_at: datetime

    goods: list[GetOrderGoodSchema]


class GetOrderList(BaseOrmSchema):
    id: int
    guid: str
    status: OrderStatusEnum
    created_at: datetime
    total_cost: float


class UpdateOrderStatusSchema(BaseModel):
    guid: str
    status: OrderStatusEnum


class OrderPageSchema(BaseModel):
    items: list[GetOrderList]
    page: int
    size: int
    pages: int
    total: int
