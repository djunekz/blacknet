import json, time
from core import engine

DATA="data"

def _logfile():
    return f"{DATA}/logs_{engine.current_target}.json"

def init_logs():
    try:
        json.load(open(_logfile()))
    except:
        json.dump({"auth.log":[], "bash_history":[]}, open(_logfile(),"w"), indent=2)

def write(log, msg):
    logs=json.load(open(_logfile()))
    logs[log].append(f"{time.ctime()} {msg}")
    json.dump(logs, open(_logfile(),"w"), indent=2)

def show(log):
    logs=json.load(open(_logfile()))
    for l in logs.get(log,[]):
        print(l)

def clear(log):
    logs=json.load(open(_logfile()))
    logs[log]=[]
    json.dump(logs, open(_logfile(),"w"), indent=2)
    print(f"[+] {log} cleared")
