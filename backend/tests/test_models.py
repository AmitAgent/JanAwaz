import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import AuditEvent, Complaint, ContactMethod, User
from app.services.complaints import create_draft_complaint


def test_user_gets_uuid(db):
    user = User(preferred_language="hi")
    db.add(user)
    db.commit()
    assert user.id is not None
    assert user.is_active is True


def test_contact_methods_are_separate_from_user(db):
    user = User()
    user.contact_methods = [
        ContactMethod(kind="email", value="a@example.com"),
        ContactMethod(kind="mobile", value="+919999999999"),
    ]
    db.add(user)
    db.commit()
    assert {c.kind for c in user.contact_methods} == {"email", "mobile"}
    assert all(c.is_verified is False for c in user.contact_methods)


def test_contact_value_unique_per_kind(db):
    u1, u2 = User(), User()
    db.add_all([u1, u2])
    db.commit()
    db.add(ContactMethod(user_id=u1.id, kind="email", value="a@example.com"))
    db.commit()
    db.add(ContactMethod(user_id=u2.id, kind="email", value="a@example.com"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_invalid_contact_kind_rejected(db):
    user = User()
    db.add(user)
    db.commit()
    db.add(ContactMethod(user_id=user.id, kind="fax", value="123"))
    with pytest.raises(IntegrityError):
        db.commit()


def test_create_and_retrieve_draft_complaint(db):
    user = User()
    db.add(user)
    db.commit()

    created = create_draft_complaint(
        db, user_id=user.id, category="power_outage", title="No power for 2 days"
    )

    fetched = db.scalar(select(Complaint).where(Complaint.id == created.id))
    assert fetched is not None
    assert fetched.status == "draft"
    assert fetched.user_id == user.id
    assert fetched.title == "No power for 2 days"


def test_draft_creation_writes_audit_event(db):
    user = User()
    db.add(user)
    db.commit()
    complaint = create_draft_complaint(db, user_id=user.id)

    events = db.scalars(select(AuditEvent)).all()
    assert len(events) == 1
    assert events[0].action == "complaint.draft_created"
    assert events[0].entity_id == complaint.id
    assert events[0].actor_user_id == user.id


def test_complaint_requires_existing_user(db):
    db.add(Complaint(user_id=uuid.uuid4(), status="draft"))
    with pytest.raises(IntegrityError):
        db.commit()
