import json, os
from core import engine, player

DATA = "data"

def ssh(user):
    if not engine.current_target:
        print("[!] no target connected")
        return

    users_file = f"{DATA}/users_{engine.current_target}.json"
    creds_file = f"{DATA}/creds_{engine.current_target}.json"

    if not os.path.exists(users_file):
        print("[!] no user database found")
        return

    if not os.path.exists(creds_file):
        print("[!] no credentials found, crack first")
        player.add_trace(1)
        return

    users = json.load(open(users_file))
    creds = json.load(open(creds_file))

    if user not in users:
        print("[!] user does not exist")
        player.add_trace(1)
        return

    if user not in creds:
        print("[!] password unknown, crack required")
        player.add_trace(1)
        return

    # PASSWORD MATCH
    if users[user]["password"] == creds[user]:
        engine.logged_user = user
        print(f"[+] logged in as {user}")
    else:
        print("[!] authentication failed")
        player.add_trace(1)
