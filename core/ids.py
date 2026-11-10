import os
import time

from core import engine
from core.paths import DATA

IDS_LOG = f"{DATA}/ids.log"


def write(event, level="INFO", target=None):
    os.makedirs(DATA, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    where = target or engine.current_target or "local"

    line = f"{ts} [{level}] target={where} event={event}\n"
    with open(IDS_LOG, "a", encoding="utf-8") as f:
        f.write(line)


def read():
    if not os.path.exists(IDS_LOG):
        print("ids: log empty")
        return

    with open(IDS_LOG, encoding="utf-8") as f:
        for line in f:
            print(line.rstrip())


def clear():
    if os.path.exists(IDS_LOG):
        os.remove(IDS_LOG)
        print("ids: log cleared")
