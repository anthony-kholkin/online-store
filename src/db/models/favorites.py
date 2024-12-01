from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.favorites_good import favorites_goods


class Favorites(BaseModel):
    __tablename__ = "favorites"

    cart_outlet_guid: Mapped[str] = mapped_column(String(255), nullable=False, primary_key=True)

    goods: Mapped[list["Good"]] = relationship("Good", secondary=favorites_goods, lazy="selectin")  # type: ignore # noqa: F821

    def __repr__(self):
        return f"<Favorites(cart_outlet_guid={self.cart_outlet_guid})>"
