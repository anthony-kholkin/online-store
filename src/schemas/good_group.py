from schemas.base import BaseOrmSchema


class GoodGroupSchema(BaseOrmSchema):
    guid: str
    name: str
    parent_group_guid: str | None = None
