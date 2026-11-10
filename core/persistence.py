from core import engine, logs, player, store
from core.paths import DATA

KEYS = ("backdoor", "cron", "service")


def _file(target=None):
    return f"{DATA}/persist_{target or engine.current_target}.json"


def _load(target=None):
    p = {k: False for k in KEYS}
    data = store.read_json(_file(target))
    if isinstance(data, dict):
        for k in KEYS:
            p[k] = bool(data.get(k))
    return p


def _save(p):
    store.write_json(_file(), p)


def install_backdoor():
    if not engine.current_target or engine.logged_user != "root":
        print("permission denied (need root)")
        return

    p = _load()
    if p["backdoor"]:
        print("backdoor already installed")
        return

    p["backdoor"] = True
    _save(p)
    logs.write("auth.log", "backdoor user created")
    print("[+] backdoor installed")


def install_cron():
    if not engine.current_target or not engine.logged_user:
        print("not logged in")
        return

    p = _load()
    if p["cron"]:
        print("cron job already exists")
        return

    p["cron"] = True
    _save(p)
    logs.write("sys.log", "cron persistence added")
    player.add_trace(1)
    print("[+] cron persistence installed")


def install_service():
    if not engine.current_target or engine.logged_user != "root":
        print("permission denied (need root)")
        return

    p = _load()
    if p["service"]:
        print("service already running")
        return

    p["service"] = True
    _save(p)
    logs.write("sys.log", "hidden service enabled")
    player.add_trace(2)
    print("[+] persistent service enabled")


def reconnect(target=None):
    target = target or engine.current_target or engine.last_target
    if not target:
        print("no previous target")
        return

    if not store.safe_name(target):
        print("invalid target name")
        return

    p = _load(target)
    if any(p.values()):
        user = "root" if p["service"] else "shell"
        engine.connect(target)
        engine.logged_user = user
        print(f"[+] reconnected to {target} via persistence")
    else:
        print("no persistence found")
