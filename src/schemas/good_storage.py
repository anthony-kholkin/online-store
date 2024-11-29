from pydantic import field_validator

from core.exceptions import incorrect_in_stock_exception
from schemas.base import BaseOrmSchema


class GoodStorageCreateSchema(BaseOrmSchema):
    good_guid: str
    specification_guid: str
    in_stock: int

    @field_validator("in_stock")
    def validate_in_stock(cls, v):
        if v < 0:
            raise incorrect_in_stock_exception
        return v


class GoodStorageGetSchema(GoodStorageCreateSchema):
    specification_name: str
