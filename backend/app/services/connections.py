import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Complaint, Connection, UserConnection
from app.services.audit import record_audit_event
from app.services.ca_number import normalize_ca_number


class ConnectionAccessDenied(Exception):
    """The user has not linked this connection."""


def _find(db: Session, discom: str, ca_normalized: str) -> Connection | None:
    return db.scalar(
        select(Connection).where(
            Connection.discom == discom, Connection.ca_number_normalized == ca_normalized
        )
    )


def link_connection(db: Session, *, user_id: uuid.UUID, discom: str, ca_number: str) -> Connection:
    """Find or create the connection and link it to the user. Safe to call repeatedly.

    Raises InvalidCANumber for a bad DISCOM or CA Number. Audit events never contain
    the CA Number; they point at the connection by its internal id.
    """
    ca = normalize_ca_number(discom, ca_number)
    connection = _find(db, discom, ca)
    if connection is None:
        try:
            with db.begin_nested():  # a lost race rolls back only this savepoint
                connection = Connection(discom=discom, ca_number_normalized=ca)
                db.add(connection)
                db.flush()
        except IntegrityError:
            connection = _find(db, discom, ca)
            if connection is None:
                raise
        else:
            record_audit_event(
                db,
                action="connection.created",
                entity_type="connection",
                entity_id=connection.id,
                actor_user_id=user_id,
                metadata={"discom": discom},
            )

    already = db.scalar(
        select(UserConnection).where(
            UserConnection.user_id == user_id, UserConnection.connection_id == connection.id
        )
    )
    if already is None:
        db.add(UserConnection(user_id=user_id, connection_id=connection.id))
        record_audit_event(
            db,
            action="connection.linked",
            entity_type="connection",
            entity_id=connection.id,
            actor_user_id=user_id,
            metadata={"discom": discom},
        )
    db.commit()
    return connection


def list_user_connections(db: Session, *, user_id: uuid.UUID) -> list[Connection]:
    return list(
        db.scalars(
            select(Connection)
            .join(UserConnection, UserConnection.connection_id == Connection.id)
            .where(UserConnection.user_id == user_id)
            .order_by(UserConnection.created_at)
        )
    )


def require_linked(db: Session, *, user_id: uuid.UUID, connection_id: uuid.UUID) -> Connection:
    connection = db.scalar(
        select(Connection)
        .join(UserConnection, UserConnection.connection_id == Connection.id)
        .where(UserConnection.user_id == user_id, Connection.id == connection_id)
    )
    if connection is None:
        raise ConnectionAccessDenied("Connection is not linked to this user")
    return connection


def list_own_complaints_for_connection(
    db: Session, *, user_id: uuid.UUID, connection_id: uuid.UUID
) -> list[Complaint]:
    """A user's own complaints on a connection they have linked.

    Linking a connection never reveals other users' complaints on it.
    """
    require_linked(db, user_id=user_id, connection_id=connection_id)
    return list(
        db.scalars(
            select(Complaint)
            .where(Complaint.user_id == user_id, Complaint.connection_id == connection_id)
            .order_by(Complaint.created_at)
        )
    )
