import json
import os
from core import engine, player
from core.logs import init_logs

DATA = "data"


def ssh(user):
    # ===== TARGET CHECK =====
    if not engine.current_target:
        print("[!] no target connected")
        return

    target = engine.current_target
    users_file = f"{DATA}/users_{target}.json"
    creds_file = f"{DATA}/creds_{target}.json"

    # ===== USER DB CHECK =====
    if not os.path.exists(users_file):
        print("[!] no user database found on target")
        return

    # ===== LOAD USER DB =====
    try:
        users = json.load(open(users_file))
    except json.JSONDecodeError:
        print("[!] corrupted user database")
        return

    # ===== USER EXISTS =====
    if user not in users:
        print("[!] user does not exist")
        player.add_trace(1)
        return

    # ===== CREDS CHECK =====
    if not os.path.exists(creds_file):
        print("[!] no credentials found, crack first")
        player.add_trace(1)
        return

    try:
        creds = json.load(open(creds_file))
    except json.JSONDecodeError:
        print("[!] corrupted credentials file")
        return

    # ===== PASSWORD KNOWN =====
    if user not in creds:
        print("[!] password unknown, crack required")
        player.add_trace(1)
        return

    # ===== AUTH =====
    real_pw = users[user].get("password")
    known_pw = creds.get(user)

    if not real_pw:
        print("[!] account misconfigured")
        return

    if real_pw == known_pw:
        engine.logged_user = user
        init_logs()
        print(f"[+] logged in as {user}")
    else:
        print("[!] authentication failed")
        player.add_trace(1)
