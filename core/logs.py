import os
import time

from core import engine, store
from core.paths import DATA


def _logfile():
    return f"{DATA}/logs_{engine.current_target}.json"


def _fresh():
    return {
        "auth.log": [],
        "bash_history": [],
        "sys.log": [],
        "_written": {}
    }


def init_logs():
    if not engine.current_target:
        return

    path = _logfile()
    os.makedirs(DATA, exist_ok=True)

    if not os.path.exists(path):
        store.write_json(path, _fresh())


def _load():
    logs = store.read_json(_logfile(), None)
    if not isinstance(logs, dict):
        logs = _fresh()
    return logs


def write(log, msg):
    init_logs()
    if not engine.current_target:
        return

    logs = _load()
    if not isinstance(logs.get(log), list):
        logs[log] = []
    logs[log].append(f"{time.ctime()} {msg}")

    written = logs.get("_written")
    if not isinstance(written, dict):
        written = logs["_written"] = {}
    written[log] = written.get(log, 0) + 1

    store.write_json(_logfile(), logs)


def show(log):
    init_logs()
    if not engine.current_target:
        return
    for entry in _load().get(log, []):
        print(entry)


def clear(log):
    init_logs()
    if not engine.current_target:
        return
    logs = _load()
    logs[log] = []
    store.write_json(_logfile(), logs)
    print(f"[+] {log} cleared")
