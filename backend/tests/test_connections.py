import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import AuditEvent, Connection, User, UserConnection
from app.services.ca_number import InvalidCANumber
from app.services.complaints import create_draft_complaint
from app.services.connections import (
    ConnectionAccessDenied,
    link_connection,
    list_own_complaints_for_connection,
    list_user_connections,
    require_linked,
)


def _user(db) -> User:
    user = User()
    db.add(user)
    db.commit()
    return user


def test_connection_unique_per_discom_and_ca(db):
    db.add(Connection(discom="SBPDCL", ca_number_normalized="123456789"))
    db.commit()
    db.add(Connection(discom="SBPDCL", ca_number_normalized="123456789"))
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()
    db.add(Connection(discom="NBPDCL", ca_number_normalized="123456789"))
    db.commit()  # same number at another DISCOM is a different connection


def test_invalid_discom_rejected_by_database(db):
    db.add(Connection(discom="XYZ", ca_number_normalized="123456789"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_link_normalizes_and_is_idempotent(db):
    user = _user(db)
    first = link_connection(db, user_id=user.id, discom="SBPDCL", ca_number="1234-56789")
    second = link_connection(db, user_id=user.id, discom="SBPDCL", ca_number=" 123456789 ")
    assert first.id == second.id
    assert first.ca_number_normalized == "123456789"
    assert len(db.scalars(select(Connection)).all()) == 1
    assert len(db.scalars(select(UserConnection)).all()) == 1


def test_two_users_share_one_connection_row(db):
    u1, u2 = _user(db), _user(db)
    c1 = link_connection(db, user_id=u1.id, discom="NBPDCL", ca_number="987654321")
    c2 = link_connection(db, user_id=u2.id, discom="NBPDCL", ca_number="987654321")
    assert c1.id == c2.id
    assert [c.id for c in list_user_connections(db, user_id=u1.id)] == [c1.id]
    assert [c.id for c in list_user_connections(db, user_id=u2.id)] == [c1.id]


def test_invalid_ca_creates_nothing(db):
    user = _user(db)
    with pytest.raises(InvalidCANumber):
        link_connection(db, user_id=user.id, discom="SBPDCL", ca_number="12")
    assert db.scalars(select(Connection)).all() == []
    assert db.scalars(select(AuditEvent)).all() == []


def test_audit_events_never_contain_the_ca_number(db):
    user = _user(db)
    link_connection(db, user_id=user.id, discom="SBPDCL", ca_number="123456789")
    events = db.scalars(select(AuditEvent)).all()
    assert {e.action for e in events} == {"connection.created", "connection.linked"}
    for event in events:
        assert "123456789" not in str(event.event_metadata)
        assert event.entity_type == "connection"
        assert event.actor_user_id == user.id


def test_second_user_link_writes_only_a_linked_event(db):
    u1, u2 = _user(db), _user(db)
    link_connection(db, user_id=u1.id, discom="SBPDCL", ca_number="123456789")
    link_connection(db, user_id=u2.id, discom="SBPDCL", ca_number="123456789")
    actions = [e.action for e in db.scalars(select(AuditEvent).order_by(AuditEvent.created_at))]
    assert actions.count("connection.created") == 1
    assert actions.count("connection.linked") == 2


def test_unlinked_user_is_denied(db):
    owner, other = _user(db), _user(db)
    conn = link_connection(db, user_id=owner.id, discom="SBPDCL", ca_number="123456789")
    with pytest.raises(ConnectionAccessDenied):
        require_linked(db, user_id=other.id, connection_id=conn.id)
    with pytest.raises(ConnectionAccessDenied):
        list_own_complaints_for_connection(db, user_id=other.id, connection_id=conn.id)


def test_linking_a_known_ca_does_not_reveal_other_users_complaints(db):
    owner, other = _user(db), _user(db)
    conn = link_connection(db, user_id=owner.id, discom="SBPDCL", ca_number="123456789")
    create_draft_complaint(db, user_id=owner.id, connection_id=conn.id, title="Owner complaint")

    # `other` only knows the CA Number; linking it still shows none of the owner's history.
    link_connection(db, user_id=other.id, discom="SBPDCL", ca_number="123456789")
    assert list_own_complaints_for_connection(db, user_id=other.id, connection_id=conn.id) == []
    owned = list_own_complaints_for_connection(db, user_id=owner.id, connection_id=conn.id)
    assert [c.title for c in owned] == ["Owner complaint"]


def test_complaint_connection_must_be_linked_to_the_user(db):
    owner, other = _user(db), _user(db)
    conn = link_connection(db, user_id=owner.id, discom="SBPDCL", ca_number="123456789")
    with pytest.raises(ConnectionAccessDenied):
        create_draft_complaint(db, user_id=other.id, connection_id=conn.id)
    assert create_draft_complaint(db, user_id=other.id).connection_id is None
