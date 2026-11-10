import os

from core import store
from core.paths import DATA

PLAYER = f"{DATA}/player.json"

DEFAULT = {
    "alias": None,
    "credits": 100,
    "rep": 0,
    "trace": 0,
    "faction": None
}


def _int(value, fallback=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def load():
    p = dict(DEFAULT)
    data = store.read_json(PLAYER)
    if isinstance(data, dict):
        p.update(data)
    for key in ("credits", "rep", "trace"):
        p[key] = _int(p.get(key), DEFAULT[key])
    if not os.path.exists(PLAYER):
        save(p)
    return p


def save(p):
    store.write_json(PLAYER, p)


def add_trace(n=1):
    p = load()
    p["trace"] = p.get("trace", 0) + n
    save(p)
    print(f"[TRACE] +{n} (current trace: {p['trace']})")
