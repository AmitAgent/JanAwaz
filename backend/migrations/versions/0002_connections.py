"""connections, user_connections, complaints.connection_id

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-20
"""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("discom", sa.String(16), nullable=False),
        sa.Column("ca_number_normalized", sa.String(32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("discom IN ('SBPDCL', 'NBPDCL')", name="discom_valid"),
        sa.PrimaryKeyConstraint("id", name="pk_connections"),
        sa.UniqueConstraint("discom", "ca_number_normalized", name="uq_connections_discom_ca"),
    )
    op.create_table(
        "user_connections",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("connection_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_user_connections_user_id_users",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["connection_id"],
            ["connections.id"],
            name="fk_user_connections_connection_id_connections",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_user_connections"),
        sa.UniqueConstraint("user_id", "connection_id", name="uq_user_connections_user_connection"),
    )
    op.create_index("ix_user_connections_user_id", "user_connections", ["user_id"])
    op.create_index("ix_user_connections_connection_id", "user_connections", ["connection_id"])

    # Batch mode so the same migration also runs on SQLite (used by the tests).
    with op.batch_alter_table("complaints") as batch:
        batch.add_column(sa.Column("connection_id", sa.Uuid(), nullable=True))
        batch.create_foreign_key(
            "fk_complaints_connection_id_connections",
            "connections",
            ["connection_id"],
            ["id"],
            ondelete="RESTRICT",
        )
        batch.create_index("ix_complaints_connection_id", ["connection_id"])


def downgrade() -> None:
    with op.batch_alter_table("complaints") as batch:
        batch.drop_index("ix_complaints_connection_id")
        batch.drop_constraint("fk_complaints_connection_id_connections", type_="foreignkey")
        batch.drop_column("connection_id")
    op.drop_table("user_connections")
    op.drop_table("connections")
