import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, String, TypeDecorator, Integer
from sqlalchemy.orm import Mapped, mapped_column


class GUID(TypeDecorator):  # type: ignore
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return str(value)


class GUIDMixin:
    """Mixin of implement guid."""

    __abstract__ = True

    guid: Mapped[str] = mapped_column(GUID(), primary_key=True, default=lambda: str(uuid.uuid4()))


class IDMixin:
    """Mixin of implement id."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)


class CreatedAtMixin:
    """Mixin to implement created_at field."""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class UpdatedAtMixin:
    """Mixin to implement updated_at field."""

    __abstract__ = True

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
