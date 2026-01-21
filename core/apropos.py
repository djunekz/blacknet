from core.man import man

INDEX = {
    "war": "faction warfare system",
    "contest": "capture network node",
    "netmap": "internal network topology",
    "stealth": "trace and detection control",
    "blue": "defensive response system",
    "persistence": "maintain access"
}

def apropos(keyword):
    found = False
    for k, v in INDEX.items():
        if keyword.lower() in k or keyword.lower() in v:
            print(f"{k:<12} - {v}")
            found = True

    if not found:
        print("nothing appropriate.")
