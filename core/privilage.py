from core import engine, logs, player, store
from core.paths import DATA


def sudo(pw):
    if not engine.logged_user:
        print("not logged in")
        return

    if not engine.current_target:
        print("no active target")
        return

    users = store.read_json(f"{DATA}/users_{engine.current_target}.json")
    if not isinstance(users, dict):
        print("[!] user database unavailable")
        return

    user = engine.logged_user

    if user not in users or not isinstance(users[user], dict):
        print("[!] user not found in database")
        return

    role = users[user].get("role", "user")

    if role == "root":
        print("[+] already root")
        return

    root_pw = users.get("root", {}).get("password", "")

    if root_pw and pw == root_pw:
        engine.logged_user = "root"
        logs.write("auth.log", "sudo to root")
        print("[+] root shell granted")
    else:
        logs.write("auth.log", "sudo failed")
        player.add_trace(1)
        print("[!] sudo failed")
