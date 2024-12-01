from schemas.base import BaseOrmSchema


class GetFavoritesGoodSchema(BaseOrmSchema):
    guid: str
    name: str
    image_key: str | None
    price: float


class GetFavoritesSchema(BaseOrmSchema):
    cart_outlet_guid: str
    goods: list[GetFavoritesGoodSchema]
