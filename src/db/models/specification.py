from db.models import Good
from db.models.base import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.good_specification import good_specifications
from db.models.mixins import GUIDMixin


class Specification(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    goods: Mapped[list["Good"]] = relationship("Good", secondary=good_specifications, back_populates="specifications")

    storages: Mapped[list["GoodStorage"]] = relationship(  # type: ignore # noqa: F821
        "GoodStorage",
        back_populates="specification",
        foreign_keys="GoodStorage.specification_guid",
    )

    prices: Mapped[list["Price"]] = relationship(  # type: ignore # noqa: F821
        "Price",
        back_populates="specification",
        foreign_keys="Price.specification_guid",
    )

    def __repr__(self):
        return f"<Specification(name={self.name})>"
