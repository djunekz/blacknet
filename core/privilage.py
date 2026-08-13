import json
from core import engine, logs, player

DATA = "data"

def sudo(pw):
    if not engine.logged_user:
        print("not logged in")
        return

    if not engine.current_target:
        print("no active target")
        return

    try:
        with open(f"{DATA}/users_{engine.current_target}.json") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("[!] user database unavailable")
        return

    user = engine.logged_user

    if user not in users:
        print("[!] user not found in database")
        return

    role = users[user].get("role", "user")

    if role == "root":
        print("[+] already root")
        return

    if pw == users.get("root", {}).get("password", ""):
        engine.logged_user = "root"
        logs.write("auth.log", "sudo to root")
        print("[+] root shell granted")
    else:
        logs.write("auth.log", "sudo failed")
        player.add_trace(1)
        print("[!] sudo failed")
