from schemas.base import BaseOrmSchema
from schemas.price_type import PriceTypeSchema
from schemas.specification import SpecificationSchema


class PriceSchema(BaseOrmSchema):
    good_guid: str
    specification_guid: str
    price_type_guid: str
    value: float


class PriceGetSchema(BaseOrmSchema):
    good_guid: str
    specification: SpecificationSchema
    price_type: PriceTypeSchema
    value: float
