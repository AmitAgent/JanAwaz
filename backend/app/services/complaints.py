import uuid

from sqlalchemy.orm import Session

from app.models import Complaint
from app.services.audit import record_audit_event


def create_draft_complaint(
    db: Session,
    *,
    user_id: uuid.UUID,
    category: str | None = None,
    title: str | None = None,
    description: str | None = None,
) -> Complaint:
    """Create a draft complaint and its audit event in one transaction."""
    complaint = Complaint(
        user_id=user_id,
        status="draft",
        category=category,
        title=title,
        description=description,
    )
    db.add(complaint)
    db.flush()  # assigns complaint.id
    record_audit_event(
        db,
        action="complaint.draft_created",
        entity_type="complaint",
        entity_id=complaint.id,
        actor_user_id=user_id,
    )
    db.commit()
    return complaint
