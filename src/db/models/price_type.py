from db.models import Price
from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class PriceType(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    prices: Mapped[list["Price"]] = relationship(
        "Price", back_populates="price_type", foreign_keys="Price.price_type_guid", lazy="selectin"
    )

    def __repr__(self):
        return f"<PriceType(name={self.name})>"
