import json, os

DATA = "data"
PLAYER = f"{DATA}/player.json"

# ===== LOAD / SAVE =====
DEFAULT = {
    "alias": None,
    "credits": 100,
    "rep": 0,
    "trace": 0,
    "faction": None
}

def load():
    if not os.path.exists(PLAYER):
        save(DEFAULT.copy())
    return json.load(open(PLAYER))

def save(p):
    os.makedirs(DATA, exist_ok=True)
    json.dump(p, open(PLAYER, "w"), indent=2)

# ===== TRACE HANDLER =====
def add_trace(n=1):
    p = load()
    p["trace"] += n
    save(p)
    print(f"[TRACE] +{n} (current trace: {p['trace']})")
