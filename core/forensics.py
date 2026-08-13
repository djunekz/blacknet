import json
import os
from core import engine

DATA = "data"


def analyze():
    if not engine.current_target:
        return 0, []

    score = 0
    iocs = []

    try:
        with open(f"{DATA}/logs_{engine.current_target}.json") as f:
            logs = json.load(f)
    except Exception:
        logs = {}

    auth   = logs.get("auth.log", [])
    syslog = logs.get("sys.log", [])

    if len(auth) >= 3:
        score += 2
        iocs.append("multiple authentication events")

    if any("failed" in l.lower() for l in auth):
        score += 1
        iocs.append("failed authentication attempts")

    if any("sudo" in l.lower() or "root" in l.lower() for l in auth):
        score += 3
        iocs.append("privilege escalation")

    if any("pivot" in l.lower() or "lateral" in l.lower() for l in auth):
        score += 3
        iocs.append("lateral movement")

    if "auth.log" in logs and logs.get("auth.log") == []:
        score += 3
        iocs.append("auth log wiped")

    if "sys.log" in logs and logs.get("sys.log") == []:
        score += 2
        iocs.append("system log wiped")

    if any("exploit" in l.lower() for l in syslog):
        score += 2
        iocs.append("exploit artifacts")

    if any("network scan" in l.lower() or "netmap" in l.lower() for l in syslog):
        score += 2
        iocs.append("network reconnaissance")

    ids_log_path = f"{DATA}/ids.log"
    idslog = []
    if os.path.exists(ids_log_path):
        with open(ids_log_path) as f:
            idslog = [
                line.strip() for line in f
                if engine.current_target in line
            ]

    if len(idslog) >= 2:
        score += 2
        iocs.append("ids alerts triggered")

    if any("HIGH" in l for l in idslog):
        score += 3
        iocs.append("high confidence intrusion")

    try:
        with open(f"{DATA}/persist_{engine.current_target}.json") as f:
            persist = json.load(f)

        if persist.get("cron"):
            score += 2
            iocs.append("cron persistence")

        if persist.get("service"):
            score += 3
            iocs.append("service persistence")

        if persist.get("backdoor"):
            score += 3
            iocs.append("backdoor installed")

    except Exception:
        pass

    if score > 10:
        score = 10

    return score, iocs
