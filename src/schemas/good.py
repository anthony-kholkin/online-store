from pydantic import BaseModel

from core.enum import GoodTypesEnum
from schemas.base import BaseOrmSchema
from schemas.good_storage import GoodStorageGetSchema
from schemas.price import PriceGetSchema
from schemas.specification import SpecificationSchema


class GoodCreateSchema(BaseOrmSchema):
    guid: str
    name: str
    description: str = ""
    good_group_guid: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR

    filling: str = ""
    aroma: str = ""
    strength: str = ""
    format: str = ""
    manufacturing_method: str = ""
    package: str = ""
    block: str = ""
    box: str = ""
    producing_country: str = ""


class GoodWithSpecsCreateSchema(GoodCreateSchema):
    specifications: list[SpecificationSchema]


class GoodGetSchema(GoodCreateSchema):
    image_key: str | None


class GoodCardGetSchema(BaseOrmSchema):
    guid: str
    name: str
    type: GoodTypesEnum = GoodTypesEnum.REGULAR
    image_key: str | None
    prices: list[PriceGetSchema]
    is_favorite: bool = False


class GoodWithSpecsGetSchema(GoodGetSchema):
    specifications: list[SpecificationSchema]
    image_key: str | None
    storages: list[GoodStorageGetSchema]


class ImageAddSchema(BaseModel):
    good_guid: str
    image: str


class GoodPageSchema(BaseModel):
    items: list[GoodCardGetSchema]
    page: int
    size: int
    pages: int
    total: int


class GoodPropertyGetSchema(BaseModel):
    name: str
    value: str = ""


class SpecificationWithPriceAndStorageSchema(BaseModel):
    good_guid: str
    specification_guid: str
    in_stock: int
    specification_name: str
    price: float


class GoodWithPropertiesGetSchema(BaseOrmSchema):
    guid: str
    name: str
    good_group_guid: str
    image_key: str | None
    is_favorite: bool = False

    description: str | None
    type: GoodTypesEnum = GoodTypesEnum.REGULAR

    properties: list[GoodPropertyGetSchema]
    specification: list[SpecificationWithPriceAndStorageSchema]
