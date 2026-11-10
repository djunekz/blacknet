import os

from core import engine, store
from core.paths import DATA


def analyze():
    if not engine.current_target:
        return 0, []

    score = 0
    iocs = []

    logs = store.read_json(f"{DATA}/logs_{engine.current_target}.json", {})
    if not isinstance(logs, dict):
        logs = {}

    auth = [l for l in logs.get("auth.log", []) if isinstance(l, str)]
    syslog = [l for l in logs.get("sys.log", []) if isinstance(l, str)]
    written = logs.get("_written", {})
    if not isinstance(written, dict):
        written = {}

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

    if written.get("auth.log", 0) > 0 and logs.get("auth.log") == []:
        score += 3
        iocs.append("auth log wiped")

    if written.get("sys.log", 0) > 0 and logs.get("sys.log") == []:
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
    token = f"target={engine.current_target} "
    if os.path.exists(ids_log_path):
        with open(ids_log_path, encoding="utf-8") as f:
            idslog = [line.strip() for line in f if token in line]

    if len(idslog) >= 2:
        score += 2
        iocs.append("ids alerts triggered")

    if any("HIGH" in l for l in idslog):
        score += 3
        iocs.append("high confidence intrusion")

    persist = store.read_json(f"{DATA}/persist_{engine.current_target}.json", {})
    if isinstance(persist, dict):
        if persist.get("cron"):
            score += 2
            iocs.append("cron persistence")

        if persist.get("service"):
            score += 3
            iocs.append("service persistence")

        if persist.get("backdoor"):
            score += 3
            iocs.append("backdoor installed")

    return min(score, 10), iocs
