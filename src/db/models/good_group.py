from db.models.base import BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import GUIDMixin


class GoodGroup(BaseModel, GUIDMixin):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_group_guid: Mapped[str | None] = mapped_column(
        String(255), ForeignKey("good_groups.guid"), nullable=True, default=None
    )

    parent_group: Mapped["GoodGroup"] = relationship(
        "GoodGroup",
        back_populates="child_groups",
        foreign_keys="GoodGroup.parent_group_guid",
    )

    child_groups: Mapped[list["GoodGroup"]] = relationship(
        "GoodGroup",
        foreign_keys="GoodGroup.parent_group_guid",
    )

    goods: Mapped[list["Good"]] = relationship(  # type: ignore # noqa: F821
        "Good",
        back_populates="good_group",
        foreign_keys="Good.good_group_guid",
    )

    def __repr__(self):
        return f"<GoodGroup(name={self.name}, parent_group_guid={self.parent_group_guid})>"
