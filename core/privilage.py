import json
from core import engine, logs, player

DATA="data"

def sudo(pw):
    users=json.load(open(f"{DATA}/users_{engine.current_target}.json"))
    user=engine.logged_user

    if not user:
        print("not logged in"); return

    if users[user]["role"]!="root" and pw=="admin123":
        engine.logged_user="root"
        logs.write("auth.log", "sudo to root")
        print("[+] root shell granted")
    else:
        logs.write("auth.log", "sudo failed")
        player.add_trace()
        print("[!] sudo failed")
