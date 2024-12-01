from db.models.base import BaseModel
from sqlalchemy import ForeignKey, Table, Column, String


favorites_goods = Table(
    "favorites_goods",
    BaseModel.metadata,
    Column("cart_outlet_guid", String(255), ForeignKey("favorites.cart_outlet_guid"), nullable=False, primary_key=True),
    Column("good_guid", String(255), ForeignKey("goods.guid"), nullable=False, primary_key=True),
)
