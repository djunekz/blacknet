import json
import os
from core import player

DATA_DIR = "data"

JOBS_FILE  = f"{DATA_DIR}/jobs.json"
TAKEN_FILE = f"{DATA_DIR}/jobs_taken.json"
DONE_FILE  = f"{DATA_DIR}/jobs_done.json"

DEFAULT_JOBS = [
    {
        "id": "JOB-001",
        "title": "Infiltrate Gov Router",
        "target": "gov-id-01",
        "objective": "capture gateway node",
        "desc": "Gain access to the government internal network via the gateway router.",
        "reward": 300,
        "rep": 2,
        "difficulty": "medium"
    },
    {
        "id": "JOB-002",
        "title": "Persistence Deployment",
        "target": "gov-id-01",
        "objective": "install backdoor",
        "desc": "Install a persistent backdoor on the target system.",
        "reward": 200,
        "rep": 1,
        "difficulty": "easy"
    },
    {
        "id": "JOB-003",
        "title": "Log Extraction",
        "target": "isp-jkt",
        "objective": "dump ISP logs",
        "desc": "Extract auth logs from the ISP node and erase evidence.",
        "reward": 250,
        "rep": 2,
        "difficulty": "medium"
    }
]


def _load(path, default):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f, indent=2)
    with open(path) as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default


def init():
    _load(JOBS_FILE, DEFAULT_JOBS)
    _load(TAKEN_FILE, [])
    _load(DONE_FILE, [])


def list_jobs():
    init()
    jobs  = _load(JOBS_FILE, [])
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    taken_ids = {j["id"] for j in taken}
    done_ids  = {j["id"] for j in done}

    print("\nAVAILABLE JOBS\n")
    for j in jobs:
        if j["id"] in done_ids:
            st = "DONE"
        elif j["id"] in taken_ids:
            st = "TAKEN"
        else:
            st = "OPEN"

        print(f"[{j['id']}] {j.get('title', j.get('desc', '?'))}")
        print(f"  target    : {j.get('target', '-')}")
        print(f"  objective : {j.get('objective', '-')}")
        print(f"  reward    : {j['reward']} credits")
        print(f"  rep       : +{j['rep']}")
        print(f"  difficulty: {j.get('difficulty', '-')}")
        print(f"  status    : {st}")
        print()


def take(job_id):
    init()
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
    print(f"    objective: {job.get('objective', '-')}")
    print(f"    target   : {job.get('target', '-')}")


def complete(job_id):
    init()
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    job = next((j for j in taken if j["id"] == job_id), None)
    if not job:
        print("[-] job not taken or not found")
        return

    p = player.load()
    p["credits"] = p.get("credits", 0) + job["reward"]
    p["rep"]     = p.get("rep", 0)     + job["rep"]
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
