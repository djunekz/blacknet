import json
import os
import urllib.request
from core import player

WORLD_URL = "https://raw.githubusercontent.com/djunekz/blacknet/main/world.json"

DATA_DIR = "data"
REPORT_DIR = f"{DATA_DIR}/reports"
CACHE_FILE = f"{DATA_DIR}/world_cache.json"
DONE_FILE  = f"{DATA_DIR}/jobs_done.json"


def pull_world():
    print("[NET] downloading world state...")
    try:
        with urllib.request.urlopen(WORLD_URL, timeout=10) as r:
            world = json.loads(r.read().decode())
    except Exception as e:
        print(f"[NET] pull failed: {e}")
        return {}

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(world, f, indent=2)

    print("[NET] world cached to", CACHE_FILE)
    return world


def push_report():
    os.makedirs(REPORT_DIR, exist_ok=True)

    p = player.load()

    done = []
    if os.path.exists(DONE_FILE):
        try:
            done = json.load(open(DONE_FILE))
        except json.JSONDecodeError:
            done = []

    report = {
        "alias": p.get("alias", "anon"),
        "rep": p.get("rep", 0),
        "trace": p.get("trace", 0),
        "completed_jobs": [j["id"] for j in done][-5:]
    }

    alias = p.get("alias") or "anon"
    fname = f"report_{abs(hash(alias)) % 99999}.json"
    path = f"{REPORT_DIR}/{fname}"

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    print("[NET] report generated:", path)
    print("[NET] submit this file via GitHub commit / PR")
