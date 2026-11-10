import hashlib
import json
import os
import ssl
import urllib.request

from core import player, store
from core.paths import DATA

WORLD_URL = "https://raw.githubusercontent.com/djunekz/blacknet/main/world.json"

DATA_DIR = DATA
REPORT_DIR = f"{DATA_DIR}/reports"
CACHE_FILE = f"{DATA_DIR}/world_cache.json"
DONE_FILE  = f"{DATA_DIR}/jobs_done.json"

MAX_WORLD_BYTES = 1_000_000


def _context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def pull_world():
    print("[NET] downloading world state...")
    try:
        with urllib.request.urlopen(WORLD_URL, timeout=10, context=_context()) as r:
            raw = r.read(MAX_WORLD_BYTES + 1)
        if len(raw) > MAX_WORLD_BYTES:
            raise ValueError("world file too large")
        world = json.loads(raw.decode("utf-8"))
    except Exception as e:
        print(f"[NET] pull failed: {e}")
        return {}

    store.write_json(CACHE_FILE, world)

    print("[NET] world cached to", CACHE_FILE)
    return world


def push_report():
    os.makedirs(REPORT_DIR, exist_ok=True)

    p = player.load()

    done = store.read_json(DONE_FILE, [])
    if not isinstance(done, list):
        done = []

    alias = p.get("alias") or "anon"

    report = {
        "alias": alias,
        "rep": p.get("rep", 0),
        "trace": p.get("trace", 0),
        "completed_jobs": [j["id"] for j in done if isinstance(j, dict) and "id" in j][-5:]
    }

    digest = hashlib.sha1(alias.encode("utf-8")).hexdigest()[:8]
    path = f"{REPORT_DIR}/report_{digest}.json"

    store.write_json(path, report)

    print("[NET] report generated:", path)
    print("[NET] submit this file via GitHub commit / PR")
