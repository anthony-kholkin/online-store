from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.enum import OrderStatusEnum
from db.models import BaseModel, GUID
from db.models.mixins import CreatedAtMixin, IDMixin

from db.models.order_good import order_goods


class Order(BaseModel, IDMixin, CreatedAtMixin):
    guid: Mapped[str] = mapped_column(GUID(), nullable=False, unique=True)
    cart_outlet_guid: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum), nullable=False)

    goods: Mapped[list["Good"]] = relationship("Good", secondary=order_goods, lazy="selectin")  # type: ignore # noqa: F821

    def __repr__(self):
        return (
            f"<Order(id={self.id}, guid={self.guid}, cart_outlet_guid={self.cart_outlet_guid}, status={self.status})>"
        )
