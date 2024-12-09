from db.models.base import BaseModel
from sqlalchemy import ForeignKey, Table, Column, Integer, String, Float

order_goods = Table(
    "order_goods",
    BaseModel.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), nullable=False, primary_key=True),
    Column("good_guid", String(255), ForeignKey("goods.guid"), nullable=False, primary_key=True),
    Column("specification_guid", ForeignKey("specifications.guid"), nullable=False, primary_key=True),
    Column("price", Float, nullable=False),
    Column("quantity", Integer, nullable=False),
)
