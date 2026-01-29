from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.store import add_job, list_jobs, update_job_status

app = FastAPI(
    title="JobTracker Job API",
    version="1.0.0"
)


# ---------- MODELS ----------
class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    job_url: Optional[str] = None
    notes: Optional[str] = None
    status: str = "saved"


class JobStatusUpdate(BaseModel):
    status: str


# ---------- ROUTES ----------
@app.get("/")
def root():
    return {
        "service": "JobTracker Job API",
        "mode": "job-tracking",
        "endpoints": [
            "POST /jobs",
            "GET /jobs",
            "PATCH /jobs/{job_id}/status"
        ]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/jobs")
def create_job(job: JobCreate):
    return add_job(job.dict())


@app.get("/jobs")
def get_jobs(title: Optional[str] = None):
    return {
        "count": len(list_jobs(title)),
        "results": list_jobs(title)
    }


@app.patch("/jobs/{job_id}/status")
def change_job_status(job_id: int, payload: JobStatusUpdate):
    try:
        return update_job_status(job_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
