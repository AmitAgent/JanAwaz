from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A citizen account. Identity only: email/mobile live in ContactMethod."""

    __tablename__ = "users"

    preferred_language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    contact_methods: Mapped[list["ContactMethod"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )
    complaints: Mapped[list["Complaint"]] = relationship(back_populates="user")  # noqa: F821
