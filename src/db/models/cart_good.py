from db.models.base import BaseModel
from sqlalchemy import ForeignKey, Table, Column, Integer, String


cart_goods = Table(
    "cart_goods",
    BaseModel.metadata,
    Column("cart_outlet_guid", String(255), ForeignKey("carts.cart_outlet_guid"), nullable=False, primary_key=True),
    Column("price_type_guid", ForeignKey("price_types.guid"), nullable=False),
    Column("good_guid", String(255), ForeignKey("goods.guid"), nullable=False, primary_key=True),
    Column("specification_guid", ForeignKey("specifications.guid"), nullable=False, primary_key=True),
    Column("quantity", Integer, nullable=False),
)
