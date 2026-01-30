from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID
import os

from .models import (
    JobApplication,
    JobApplicationCreate,
    JobApplicationUpdate,
    StatusHistory
)
from .store import (
    create_application,
    list_applications,
    update_application_status,
    get_history,
    applications
)

app = FastAPI(
    title="Job Tracker API",
    version="1.0.0"
)

# CORS (local + future ingress)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "job-api",
        "environment": os.getenv("APP_ENV", "local")
    }

@app.post("/applications", response_model=JobApplication, status_code=201)
def create_app(payload: JobApplicationCreate):
    return create_application(payload)

@app.get("/applications", response_model=list[JobApplication])
def list_apps():
    return list_applications()

@app.patch("/applications/{app_id}", response_model=JobApplication)
def update_status(app_id: UUID, payload: JobApplicationUpdate):
    if app_id not in applications:
        raise HTTPException(status_code=404, detail="Application not found")
    return update_application_status(app_id, payload)

@app.get("/applications/{app_id}/history", response_model=list[StatusHistory])
def history_view(app_id: UUID):
    return get_history(app_id)
