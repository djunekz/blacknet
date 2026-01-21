import json
import os

JOBS_FILE = "data/jobs.json"
TAKEN_FILE = "data/jobs_taken.json"

def take_job(job_id):
    if not os.path.exists(JOBS_FILE):
        print("Jobs database missing.")
        return

    with open(JOBS_FILE) as f:
        jobs = json.load(f)

    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        print("Job not found.")
        return

    if not os.path.exists(TAKEN_FILE):
        with open(TAKEN_FILE, "w") as f:
            json.dump([], f)

    with open(TAKEN_FILE) as f:
        taken = json.load(f)

    if any(j["id"] == job_id for j in taken):
        print("Job already taken.")
        return

    taken.append(job)

    with open(TAKEN_FILE, "w") as f:
        json.dump(taken, f, indent=2)

    print(f"Job {job_id} taken.")
