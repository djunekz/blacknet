import os, time
from core import engine

DATA = "data"
IDS_LOG = f"{DATA}/ids.log"

def write(event, level="INFO"):
    os.makedirs(DATA, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    target = engine.current_target or "local"

    line = f"{ts} [{level}] target={target} event={event}\n"
    with open(IDS_LOG, "a") as f:
        f.write(line)

def read():
    if not os.path.exists(IDS_LOG):
        print("ids: log empty")
        return

    with open(IDS_LOG) as f:
        for line in f:
            print(line.rstrip())

def clear():
    if os.path.exists(IDS_LOG):
        os.remove(IDS_LOG)
        print("ids: log cleared")
