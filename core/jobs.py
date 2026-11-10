import os

from core import player, store
from core.paths import DATA

DATA_DIR = DATA

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
    },
    {
        "id": "JOB-004",
        "title": "Shadow Banking",
        "target": "gov-id-01",
        "objective": "pivot to internal-db",
        "desc": "Reach the internal database node inside the government network.",
        "reward": 500,
        "rep": 4,
        "difficulty": "hard"
    }
]


def _num(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _reward(job):
    r = job.get("reward", 0)
    if isinstance(r, dict):
        return _num(r.get("credits", 0)), _num(r.get("rep", job.get("rep", 0)))
    return _num(r), _num(job.get("rep", 0))


def _load(path, default):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        store.write_json(path, default)
        return list(default)
    data = store.read_json(path, default)
    if not isinstance(data, list):
        return list(default)
    return [j for j in data if isinstance(j, dict) and "id" in j]


def _find(items, job_id):
    wanted = str(job_id).casefold()
    return next((j for j in items if str(j["id"]).casefold() == wanted), None)


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

        credits, rep = _reward(j)
        print(f"[{j['id']}] {j.get('title', j.get('desc', '?'))}")
        print(f"  target    : {j.get('target', '-')}")
        print(f"  objective : {j.get('objective', '-')}")
        print(f"  reward    : {credits} credits")
        print(f"  rep       : +{rep}")
        print(f"  difficulty: {j.get('difficulty', '-')}")
        print(f"  status    : {st}")
        print()


def take(job_id):
    init()
    jobs  = _load(JOBS_FILE, [])
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    job = _find(jobs, job_id)
    if not job:
        print("[-] job not found")
        return

    if _find(taken, job["id"]):
        print("[-] job already taken")
        return

    if _find(done, job["id"]):
        print("[-] job already completed")
        return

    taken.append(job)
    store.write_json(TAKEN_FILE, taken)

    print(f"[+] job {job['id']} accepted")
    print(f"    objective: {job.get('objective', '-')}")
    print(f"    target   : {job.get('target', '-')}")


def complete(job_id):
    init()
    taken = _load(TAKEN_FILE, [])
    done  = _load(DONE_FILE, [])

    job = _find(taken, job_id)
    if not job:
        print("[-] job not taken or not found")
        return

    credits, rep = _reward(job)

    p = player.load()
    p["credits"] = p.get("credits", 0) + credits
    p["rep"]     = p.get("rep", 0)     + rep
    player.save(p)

    taken = [j for j in taken if j["id"] != job["id"]]
    done.append(job)

    store.write_json(TAKEN_FILE, taken)
    store.write_json(DONE_FILE, done)

    print(f"[✓] job {job['id']} completed")
    print(f"    +{credits} credits")
    print(f"    +{rep} reputation")
