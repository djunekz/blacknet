import json, time
from core import engine, logs, player

DATA="data"

def _file():
    return f"{DATA}/persist_{engine.current_target}.json"

def _load():
    try:
        return json.load(open(_file()))
    except:
        return {"backdoor": False, "cron": False, "service": False}

def _save(p):
    json.dump(p, open(_file(),"w"), indent=2)

# -------- BACKDOOR --------
def install_backdoor():
    if engine.logged_user != "root":
        print("permission denied (need root)")
        return

    p=_load()
    if p["backdoor"]:
        print("backdoor already installed")
        return

    p["backdoor"]=True
    _save(p)
    logs.write("auth.log", "backdoor user created")
    print("[+] backdoor installed")

# -------- CRON --------
def install_cron():
    if not engine.logged_user:
        print("not logged in")
        return

    p=_load()
    if p["cron"]:
        print("cron job already exists")
        return

    p["cron"]=True
    _save(p)
    logs.write("sys.log", "cron persistence added")
    player.add_trace(1)
    print("[+] cron persistence installed")

# -------- SERVICE --------
def install_service():
    if engine.logged_user != "root":
        print("permission denied (need root)")
        return

    p=_load()
    if p["service"]:
        print("service already running")
        return

    p["service"]=True
    _save(p)
    logs.write("sys.log", "hidden service enabled")
    player.add_trace(2)
    print("[+] persistent service enabled")

# -------- RECONNECT --------
def reconnect():
    p=_load()
    if p["backdoor"] or p["cron"] or p["service"]:
        engine.logged_user="root" if p["service"] else "shell"
        engine.cwd="/"
        print("[+] reconnected via persistence")
    else:
        print("no persistence found")
