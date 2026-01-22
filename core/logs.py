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

    if not os.path.exists(DATA):
        os.makedirs(DATA)

    if not os.path.exists(path):
        json.dump(
            {
                "auth.log": [],
                "bash_history": [],
                "system.log": []
            },
            open(path, "w"),
            indent=2
        )


def write(log, msg):
    init_logs()
    logs = json.load(open(_logfile()))

    if log not in logs:
        logs[log] = []

    logs[log].append(f"{time.ctime()} {msg}")
    json.dump(logs, open(_logfile(), "w"), indent=2)


def show(log):
    init_logs()
    logs = json.load(open(_logfile()))
    for l in logs.get(log, []):
        print(l)


def clear(log):
    init_logs()
    logs = json.load(open(_logfile()))
    logs[log] = []
    json.dump(logs, open(_logfile(), "w"), indent=2)
    print(f"[+] {log} cleared")
