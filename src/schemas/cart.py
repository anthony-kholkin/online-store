from pydantic import BaseModel, field_validator

from core.exceptions import invalid_quantity_exception
from schemas.base import BaseOrmSchema


class GetBaseCartSchema(BaseOrmSchema):
    cart_outlet_guid: str


class AddOrUpdateGoodToCartSchema(BaseModel):
    good_guid: str
    specification_guid: str
    price_type_guid: str
    quantity: int

    @field_validator("quantity")
    def validate_sum(cls, v):
        if v <= 0:
            raise invalid_quantity_exception

        return v


class GetCartGoodSchema(BaseOrmSchema):
    guid: str
    specification_guid: str
    price_type_guid: str
    name: str
    image_key: str | None
    is_favorite: bool
    quantity: int
    price: float


class GetCartSchema(GetBaseCartSchema):
    goods: list[GetCartGoodSchema]
    total_cost: float




class CartGoodSchema(BaseOrmSchema):
    cart_outlet_guid: str
    price_type_guid: str
    good_guid: str
    specification_guid: str
    quantity: int


class LightCartGoodSchema(BaseOrmSchema):
    cart_outlet_guid: str
    good_guid: str
    specification_guid: str
    quantity: int


class DeleteGoodSchema(GetBaseCartSchema):
    good_guid: str
    specification_guid: str
