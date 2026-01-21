import json
from core import engine

DATA = "data"

def analyze():
    """
    Melakukan analisis forensik berbasis log & artefak
    Return:
      score : int
      iocs  : list[str]
    """

    if not engine.current_target:
        return 0, []

    score = 0
    iocs = []

    # ===== LOAD LOG =====
    try:
        logs = json.load(open(f"{DATA}/logs_{engine.current_target}.json"))
    except:
        logs = {}

    auth = logs.get("auth.log", [])
    syslog = logs.get("sys.log", [])
    idslog = logs.get("ids.log", [])

    # ===== AUTH EVENTS =====
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

    # ===== LOG TAMPERING =====
    if "auth.log" in logs and logs.get("auth.log") == []:
        score += 3
        iocs.append("auth log wiped")

    if "sys.log" in logs and logs.get("sys.log") == []:
        score += 2
        iocs.append("system log wiped")

    # ===== SYSTEM EVENTS =====
    if any("exploit" in l.lower() for l in syslog):
        score += 2
        iocs.append("exploit artifacts")

    if any("network scan" in l.lower() or "netmap" in l.lower() for l in syslog):
        score += 2
        iocs.append("network reconnaissance")

    # ===== IDS EVENTS =====
    if len(idslog) >= 2:
        score += 2
        iocs.append("ids alerts triggered")

    if any("HIGH" in l for l in idslog):
        score += 3
        iocs.append("high confidence intrusion")

    # ===== PERSISTENCE =====
    try:
        persist = json.load(open(f"{DATA}/persist_{engine.current_target}.json"))
        if persist.get("cron"):
            score += 2
            iocs.append("cron persistence")

        if persist.get("service"):
            score += 3
            iocs.append("service persistence")

        if persist.get("ssh_key"):
            score += 3
            iocs.append("ssh key persistence")

    except:
        pass

    # ===== SCORE CEILING =====
    if score > 10:
        score = 10

    return score, iocs
