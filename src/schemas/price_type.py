from schemas.base import BaseOrmSchema


class PriceTypeSchema(BaseOrmSchema):
    name: str
    guid: str
