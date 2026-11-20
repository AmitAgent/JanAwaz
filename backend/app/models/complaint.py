import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Complaint(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """A citizen complaint. Drafts only for now.

    `connection_id` is optional: a draft may exist before the citizen picks a connection.
    The service layer only allows a connection the complaint's user has linked.
    """

    __tablename__ = "complaints"
    __table_args__ = (CheckConstraint("status IN ('draft')", name="status_valid"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    connection_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("connections.id", ondelete="RESTRICT"), index=True, nullable=True
    )
    status: Mapped[str] = mapped_column(String(32), default="draft", nullable=False)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="complaints")  # noqa: F821
