from core import engine, player
from core.faction import get_faction
import json, os

DATA = "data"

def status():
    p = player.load()
    faction = get_faction()

    print("\n=== STATUS REPORT ===")

    # ===== PLAYER =====
    print("\n[PLAYER]")
    print(f" Alias     : {p.get('alias', 'unknown')}")
    print(f" Faction   : {faction or '-'}")
    print(f" Credits   : {p.get('credits', 0)}")
    print(f" Reputation: {p.get('rep', 0)}")
    print(f" Trace     : {p.get('trace', 0)}")

    # ===== TARGET =====
    print("\n[TARGET]")
    if not engine.current_target:
        print(" Not connected")
    else:
        print(f" Target    : {engine.current_target}")
        print(f" User      : {engine.logged_user or 'shell'}")
        print(f" Directory : {engine.cwd}")

    # ===== WAR / FACTION =====
    print("\n[WAR]")
    if not engine.current_target:
        print(" No active battlefield")
    else:
        path = f"{DATA}/network_{engine.current_target}.json"
        if not os.path.exists(path):
            print(" No network data")
        else:
            net = json.load(open(path))
            total = len(net.get("nodes", {}))
            owned = sum(
                1 for n in net["nodes"].values()
                if n.get("owner") == faction
            )
            print(f" Nodes owned: {owned}/{total}")

    # ===== STEALTH =====
    print("\n[STEALTH]")
    trace = p.get("trace", 0)
    if trace < 3:
        level = "LOW"
    elif trace < 6:
        level = "MEDIUM"
    elif trace < 9:
        level = "HIGH"
    else:
        level = "CRITICAL"

    print(f" Detection level: {level}")

    print("\n=====================\n")
