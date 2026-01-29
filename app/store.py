from datetime import datetime
from typing import List, Dict
import itertools

_job_id_counter = itertools.count(1)
_jobs: List[Dict] = []


def add_job(job: Dict) -> Dict:
    job["id"] = next(_job_id_counter)
    job["created_at"] = datetime.utcnow().isoformat()
    job["updated_at"] = job["created_at"]
    _jobs.append(job)
    return job


def list_jobs(title: str | None = None) -> List[Dict]:
    if not title:
        return _jobs

    title_lower = title.lower()
    return [j for j in _jobs if title_lower in j["title"].lower()]


def update_job_status(job_id: int, status: str) -> Dict:
    for job in _jobs:
        if job["id"] == job_id:
            job["status"] = status
            job["updated_at"] = datetime.utcnow().isoformat()
            return job
    raise ValueError("Job not found")
