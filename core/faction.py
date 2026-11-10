from core import store
from core.paths import DATA

PROFILE = f"{DATA}/profile.json"

FACTIONS = {
    "red": {
        "name": "RED Hat Hacker",
        "desc": "offensive / underground",
    },
    "blue": {
        "name": "BLUE Hat Hacker",
        "desc": "defensive / forensics",
    },
    "gray": {
        "name": "GRAY Hat Hacker",
        "desc": "freelancer / neutral",
    }
}


def load_profile():
    data = store.read_json(PROFILE, {})
    return data if isinstance(data, dict) else {}


def save_profile(p):
    store.write_json(PROFILE, p)


def get_faction():
    f = load_profile().get("faction")
    return f if f in FACTIONS else None


def choose_faction():
    print("Choose your faction:\n")
    for k, v in FACTIONS.items():
        print(f"  {k}  → {v['name']} ({v['desc']})")

    while True:
        try:
            f = input("> ").strip().lower()
        except KeyboardInterrupt:
            print("\n[EXIT] faction selection aborted.")
            return None

        if f in FACTIONS:
            p = load_profile()
            p["faction"] = f
            save_profile(p)
            return f

        print("Invalid faction. Choose: red / blue / gray")
