from pydantic import BaseModel


class OutletSchema(BaseModel):
    guid: str
    name: str
    price_type_guid: str
