import uuid

from sqlalchemy.orm import Session

from app.models import Complaint
from app.services.audit import record_audit_event
from app.services.connections import require_linked


def create_draft_complaint(
    db: Session,
    *,
    user_id: uuid.UUID,
    connection_id: uuid.UUID | None = None,
    category: str | None = None,
    title: str | None = None,
    description: str | None = None,
) -> Complaint:
    """Create a draft complaint and its audit event in one transaction.

    If `connection_id` is given, the user must have linked that connection
    (raises ConnectionAccessDenied otherwise).
    """
    if connection_id is not None:
        require_linked(db, user_id=user_id, connection_id=connection_id)
    complaint = Complaint(
        user_id=user_id,
        connection_id=connection_id,
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
