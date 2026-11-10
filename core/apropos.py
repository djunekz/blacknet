INDEX = {
    "war": "faction warfare system",
    "contest": "capture network node",
    "netmap": "internal network topology",
    "stealth": "trace and detection control",
    "blue": "defensive response system",
    "persistence": "maintain access",
    "pivot": "lateral movement between nodes",
    "crack": "brute-force a user password",
    "jobs": "community contracts",
    "sudo": "become root",
    "lay-low": "reduce trace",
    "ids": "intrusion detection log"
}

def apropos(keyword):
    found = False
    for k, v in INDEX.items():
        if keyword.lower() in k or keyword.lower() in v:
            print(f"{k:<12} - {v}")
            found = True

    if not found:
        print("nothing appropriate.")
