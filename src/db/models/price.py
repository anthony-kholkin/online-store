from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String, Float, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Price(BaseModel):
    good_guid: Mapped[str] = mapped_column(String(255), ForeignKey("goods.guid"), nullable=False, primary_key=True)
    specification_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("specifications.guid"), nullable=False, primary_key=True
    )
    price_type_guid: Mapped[str] = mapped_column(
        String(255), ForeignKey("price_types.guid"), nullable=False, primary_key=True
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)

    good: Mapped["Good"] = relationship(  # type: ignore # noqa: F821
        "Good",
        back_populates="prices",
        foreign_keys="Price.good_guid",
    )
    specification: Mapped["Specification"] = relationship(  # type: ignore # noqa: F821
        "Specification", foreign_keys="Price.specification_guid", back_populates="prices", lazy="selectin"
    )
    price_type: Mapped["PriceType"] = relationship(  # type: ignore # noqa: F821
        "PriceType", foreign_keys="Price.price_type_guid", back_populates="prices", lazy="selectin"
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "good_guid",
            "specification_guid",
            "price_type_guid",
            name="good_spec_price_type_constraint",
        ),
    )

    def __repr__(self):
        return (
            f"<Price(good_guid={self.good_guid}, specification_guid='{self.specification_guid}', "
            f"price_type_guid='{self.price_type_guid}', , value='{self.value}')>"
        )
