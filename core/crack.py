import os
import time

from core import store
from core.ids import write
from core.paths import DATA


def crack(target, user):
    if not store.safe_name(target):
        print("[CRACK] invalid target name")
        return

    write(f"password cracking on {target}:{user}", "MEDIUM", target=target)

    users_path = f"{DATA}/users_{target}.json"
    creds_path = f"{DATA}/creds_{target}.json"
    wordlist_path = f"{DATA}/wordlist.txt"

    if not os.path.exists(users_path):
        print(f"[CRACK] no user database for target '{target}'")
        return

    if not os.path.exists(wordlist_path):
        print("[CRACK] wordlist not found")
        return

    users = store.read_json(users_path)
    if not isinstance(users, dict):
        print("[CRACK] corrupted user database")
        return

    if user not in users:
        print(f"[CRACK] user '{user}' not found on {target}")
        return

    password = users[user].get("password") if isinstance(users[user], dict) else None
    if not password:
        print("[CRACK] password field missing")
        return

    creds = store.read_json(creds_path, {})
    if not isinstance(creds, dict):
        creds = {}

    if user in creds:
        print(f"[CRACK] password already known for {user}@{target}")
        return

    print(f"[CRACK] bruteforcing {user}@{target}...")

    with open(wordlist_path, encoding="utf-8", errors="replace") as f:
        for w in f:
            w = w.strip()
            if not w:
                continue

            time.sleep(0.2)
            print(f"trying {w}")

            if w == password:
                print(f"[+] PASSWORD FOUND → {user}@{target} : {w}")
                creds[user] = w
                store.write_json(creds_path, creds)
                return

    print("[!] crack failed")
