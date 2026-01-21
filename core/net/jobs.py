import json, os

JOBS="data/jobs.json"

def load_jobs():
    if not os.path.exists(JOBS):
        json.dump([], open(JOBS,"w"))
    return json.load(open(JOBS))

def list_jobs():
    for j in load_jobs():
        print(f"{j['id']} | {j['target']} | reward:{j['reward']}")

def take(job_id):
    jobs = load_jobs()
    for j in jobs:
        if j["id"] == job_id:
            print(f"[JOB] accepted {job_id}")
            return j
    print("job not found")
