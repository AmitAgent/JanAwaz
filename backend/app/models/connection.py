from sqlalchemy import CheckConstraint, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin

DISCOMS = ("SBPDCL", "NBPDCL")


class Connection(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """An electricity connection: one DISCOM plus a normalized CA Number.

    The (discom, ca_number_normalized) pair is unique across the platform.
    Knowing a CA Number never grants access to anything: see UserConnection.
    """

    __tablename__ = "connections"
    __table_args__ = (
        UniqueConstraint("discom", "ca_number_normalized", name="uq_connections_discom_ca"),
        CheckConstraint("discom IN ('SBPDCL', 'NBPDCL')", name="discom_valid"),
    )

    discom: Mapped[str] = mapped_column(String(16), nullable=False)
    ca_number_normalized: Mapped[str] = mapped_column(String(32), nullable=False)
