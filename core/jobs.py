import json
import os
from core import player

DATA_DIR = "data"

JOBS_FILE = f"{DATA_DIR}/jobs.json"          # global (GitHub)
TAKEN_FILE = f"{DATA_DIR}/jobs_taken.json"   # local player
DONE_FILE  = f"{DATA_DIR}/jobs_done.json"    # local player


# =========================
# INIT FILES (SAFE)
# =========================
def _load(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2)
    with open(path) as f:
        return json.load(f)


def init():
    os.makedirs(DATA_DIR, exist_ok=True)

    _load(JOBS_FILE, [
        {
            "id": "JOB-001",
            "desc": "dump ISP logs",
            "reward": 200,
            "rep": 1
        },
        {
            "id": "JOB-002",
            "desc": "deface corp site",
            "reward": 300,
            "rep": 2
        }
    ])

    _load(TAKEN_FILE, [])
    _load(DONE_FILE, [])


# =========================
# LIST JOBS
# =========================
def list_jobs():
    jobs = _load(JOBS_FILE, [])
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    taken_ids = {j["id"] for j in taken}
    done_ids  = {j["id"] for j in done}

    print("\nAVAILABLE JOBS\n")
    for j in jobs:
        if j["id"] in done_ids:
            status = "DONE"
        elif j["id"] in taken_ids:
            status = "TAKEN"
        else:
            status = "OPEN"

        print(f"[{j['id']}] {j['desc']}")
        print(f"  reward : {j['reward']} credits")
        print(f"  rep    : +{j['rep']}")
        print(f"  status : {status}")
        print()


# =========================
# TAKE JOB
# =========================
def take(job_id):
    jobs  = _load(JOBS_FILE, [])
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    if any(j["id"] == job_id for j in taken):
        print("[-] job already taken")
        return

    if any(j["id"] == job_id for j in done):
        print("[-] job already completed")
        return

    job = next((j for j in jobs if j["id"] == job_id), None)
    if not job:
        print("[-] job not found")
        return

    taken.append(job)
    with open(TAKEN_FILE, "w") as f:
        json.dump(taken, f, indent=2)

    print(f"[+] job {job_id} accepted")


# =========================
# COMPLETE JOB
# =========================
def complete(job_id):
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    job = next((j for j in taken if j["id"] == job_id), None)
    if not job:
        print("[-] job not taken")
        return

    p = player.load()
    p["credits"] += job["reward"]
    p["rep"] += job["rep"]
    player.save(p)

    taken = [j for j in taken if j["id"] != job_id]
    done.append(job)

    with open(TAKEN_FILE, "w") as f:
        json.dump(taken, f, indent=2)
    with open(DONE_FILE, "w") as f:
        json.dump(done, f, indent=2)

    print(f"[✓] job {job_id} completed")
    print(f"    +{job['reward']} credits")
    print(f"    +{job['rep']} reputation")
