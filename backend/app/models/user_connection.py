import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class UserConnection(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Links a user to a connection they have claimed.

    Many users may link to the same connection. A link lets a user attach their
    own complaints to it; it never exposes other users' complaints.
    """

    __tablename__ = "user_connections"
    __table_args__ = (
        UniqueConstraint("user_id", "connection_id", name="uq_user_connections_user_connection"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("connections.id", ondelete="RESTRICT"), index=True, nullable=False
    )
