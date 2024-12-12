from schemas.base import BaseOrmSchema


class GetFavoritesGoodSchema(BaseOrmSchema):
    guid: str
    name: str
    image_key: str | None
    price: float


class BaseFavoritesSchema(BaseOrmSchema):
    cart_outlet_guid: str


class GetFavoritesSchema(BaseFavoritesSchema):
    goods: list[GetFavoritesGoodSchema]


class AddFavoritesSchema(GetFavoritesGoodSchema):
    cart_outlet_guid: str


class AddOrDeleteFavoritesSchema(BaseFavoritesSchema):
    good_guid: str
