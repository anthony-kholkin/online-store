from sqlalchemy import ForeignKey

from db.models.base import BaseModel
from sqlalchemy import Table, Column

good_specifications = Table(
    "good_specifications",
    BaseModel.metadata,
    Column("good_guid", ForeignKey("goods.guid"), primary_key=True),
    Column("specification_guid", ForeignKey("specifications.guid"), primary_key=True),
)
