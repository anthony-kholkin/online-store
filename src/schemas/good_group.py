from schemas.base import BaseOrmSchema


class GoodGroupSchema(BaseOrmSchema):
    guid: str
    name: str
    parent_group_guid: str | None = None


class GetGoodGroupSchema(BaseOrmSchema):
    guid: str
    name: str


class GetTreeGoodGroupSchema(BaseOrmSchema):
    guid: str
    name: str
    parent_group_guid: str | None = None
    child_groups: list["GetTreeGoodGroupSchema"] = []
