from typing import Dict, List
from uuid import UUID, uuid4
from datetime import datetime

from .models import (
    JobApplication,
    JobApplicationCreate,
    JobApplicationUpdate,
    StatusHistory
)

applications: Dict[UUID, JobApplication] = {}
history: List[StatusHistory] = []


def create_application(data: JobApplicationCreate) -> JobApplication:
    app = JobApplication(
        id=uuid4(),
        company=data.company,
        role=data.role,
        location=data.location,
        status="APPLIED",
        created_at=datetime.utcnow()
    )
    applications[app.id] = app
    return app


def list_applications() -> List[JobApplication]:
    return list(applications.values())


def update_application_status(app_id: UUID, update: JobApplicationUpdate) -> JobApplication:
    app = applications[app_id]
    old_status = app.status
    app.status = update.status

    history.append(
        StatusHistory(
            application_id=app_id,
            old_status=old_status,
            new_status=update.status,
            changed_at=datetime.utcnow()
        )
    )
    return app


def get_history(app_id: UUID) -> List[StatusHistory]:
    return [h for h in history if h.application_id == app_id]
