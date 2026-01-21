import json, os

PROFILE = "data/profile.json"

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
    if not os.path.exists(PROFILE):
        return {}
    return json.load(open(PROFILE))

def save_profile(p):
    os.makedirs("data", exist_ok=True)
    json.dump(p, open(PROFILE, "w"), indent=2)

def get_faction():
    return load_profile().get("faction")

def choose_faction():
    print("Choose your faction:\n")
    for k,v in FACTIONS.items():
        print(f"  {k}  → {v['name']} ({v['desc']})")

    while True:
        try:
            f = input("> ").strip().lower()
        except KeyboardInterrupt:
            print("\n[EXIT] faction selection aborted.")
            return None

        if f in ("red", "blue", "gray"):
            p = load_profile()
            p["faction"] = f
            save_profile(p)
            return f

        print("Invalid faction. Choose: red / blue / gray")

