import json
import time
import os
from core import engine

DATA = "data"


def _logfile():
    return f"{DATA}/logs_{engine.current_target}.json"


def init_logs():
    if not engine.current_target:
        return

    path = _logfile()

    os.makedirs(DATA, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(
                {
                    "auth.log": [],
                    "bash_history": [],
                    "sys.log": []
                },
                f,
                indent=2
            )


def write(log, msg):
    init_logs()
    if not engine.current_target:
        return
    with open(_logfile()) as f:
        logs = json.load(f)

    if log not in logs:
        logs[log] = []

    logs[log].append(f"{time.ctime()} {msg}")

    with open(_logfile(), "w") as f:
        json.dump(logs, f, indent=2)


def show(log):
    init_logs()
    if not engine.current_target:
        return
    with open(_logfile()) as f:
        logs = json.load(f)
    for entry in logs.get(log, []):
        print(entry)


def clear(log):
    init_logs()
    if not engine.current_target:
        return
    with open(_logfile()) as f:
        logs = json.load(f)
    logs[log] = []
    with open(_logfile(), "w") as f:
        json.dump(logs, f, indent=2)
    print(f"[+] {log} cleared")
