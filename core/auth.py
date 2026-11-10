import os

from core import engine, player, store
from core.logs import init_logs
from core.paths import DATA


def ssh(user):
    if not engine.current_target:
        print("[!] no target connected")
        return

    target = engine.current_target
    users_file = f"{DATA}/users_{target}.json"
    creds_file = f"{DATA}/creds_{target}.json"

    if not os.path.exists(users_file):
        print("[!] no user database found on target")
        return

    users = store.read_json(users_file)
    if not isinstance(users, dict):
        print("[!] corrupted user database")
        return

    if user not in users:
        print("[!] user does not exist")
        player.add_trace(1)
        return

    if not os.path.exists(creds_file):
        print("[!] no credentials found, crack first")
        player.add_trace(1)
        return

    creds = store.read_json(creds_file)
    if not isinstance(creds, dict):
        print("[!] corrupted credentials file")
        return

    if user not in creds:
        print("[!] password unknown, crack required")
        player.add_trace(1)
        return

    real_pw = users[user].get("password") if isinstance(users[user], dict) else None
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
