import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

CONTACT_KINDS = ("email", "mobile")


class ContactMethod(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """An email or mobile number belonging to a user.

    `value` must be stored in normalized form (lowercase email, E.164 mobile).
    Normalization and encryption/hashing are added with the OTP work in Phase 2.
    """

    __tablename__ = "contact_methods"
    __table_args__ = (
        UniqueConstraint("kind", "value", name="uq_contact_methods_kind_value"),
        CheckConstraint("kind IN ('email', 'mobile')", name="kind_valid"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    kind: Mapped[str] = mapped_column(String(16), nullable=False)
    value: Mapped[str] = mapped_column(String(320), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="contact_methods")  # noqa: F821
