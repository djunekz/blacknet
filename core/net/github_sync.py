import json
import os
import urllib.request
from core import player

# === GANTI SESUAI REPO KAMU ===
WORLD_URL = "https://raw.githubusercontent.com/djunekz/blacknet/main/world.json"

DATA_DIR = "data"
REPORT_DIR = f"{DATA_DIR}/reports"
CACHE_FILE = f"{DATA_DIR}/world_cache.json"


def pull_world():
    print("[NET] downloading world state...")
    with urllib.request.urlopen(WORLD_URL, timeout=10) as r:
        world = json.loads(r.read().decode())

    os.makedirs(DATA_DIR, exist_ok=True)
    json.dump(world, open(CACHE_FILE, "w"), indent=2)

    print("[NET] world cached to", CACHE_FILE)
    return world


def push_report():
    os.makedirs(REPORT_DIR, exist_ok=True)

    report = {
        "alias": player.alias,
        "rep": player.rep,
        "trace": player.trace,
        "completed_jobs": player.completed_jobs[-5:]
    }

    fname = f"report_{abs(hash(player.alias)) % 99999}.json"
    path = f"{REPORT_DIR}/{fname}"

    json.dump(report, open(path, "w"), indent=2)

    print("[NET] report generated:", path)
    print("[NET] submit this file via GitHub commit / PR")
