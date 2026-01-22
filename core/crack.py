import time
import json
import os
from core.ids import write

DATA = "data"


def crack(target, user):
    # IDS LOG
    write(f"password cracking on {target}:{user}", "MEDIUM")

    users_path = f"{DATA}/users_{target}.json"
    creds_path = f"{DATA}/creds_{target}.json"
    wordlist_path = f"{DATA}/wordlist.txt"

    # === CHECK FILES ===
    if not os.path.exists(users_path):
        print(f"[CRACK] no user database for target '{target}'")
        return

    if not os.path.exists(wordlist_path):
        print("[CRACK] wordlist not found")
        return

    # === LOAD USERS ===
    try:
        users = json.load(open(users_path))
    except json.JSONDecodeError:
        print("[CRACK] corrupted user database")
        return

    if user not in users:
        print(f"[CRACK] user '{user}' not found on {target}")
        return

    password = users[user].get("password")
    if not password:
        print("[CRACK] password field missing")
        return

    # === LOAD CREDS (IF ANY) ===
    creds = {}
    if os.path.exists(creds_path):
        try:
            creds = json.load(open(creds_path))
        except json.JSONDecodeError:
            creds = {}

    # === ALREADY CRACKED ===
    if user in creds:
        print(f"[CRACK] password already known for {user}@{target}")
        return

    print(f"[CRACK] bruteforcing {user}@{target}...")

    # === BRUTEFORCE ===
    for w in open(wordlist_path):
        w = w.strip()
        if not w:
            continue

        time.sleep(0.2)
        print(f"trying {w}")

        if w == password:
            print(f"[+] PASSWORD FOUND → {user}@{target} : {w}")

            # === SAVE CREDS ===
            creds[user] = w
            json.dump(creds, open(creds_path, "w"), indent=2)

            return

    print("[!] crack failed")
