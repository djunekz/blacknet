from core import engine, player
from core.faction import get_faction
from core import store
from core.paths import DATA

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
        if engine.current_node:
            print(f" Node      : {engine.current_node}")
        print(f" User      : {engine.logged_user or 'shell'}")
        print(f" Directory : {engine.cwd}")

    # ===== WAR / FACTION =====
    print("\n[WAR]")
    if not engine.current_target:
        print(" No active battlefield")
    else:
        net = store.read_json(f"{DATA}/network_{engine.current_target}.json")
        if not isinstance(net, dict) or not isinstance(net.get("nodes"), dict):
            print(" No network data")
        else:
            nodes = net["nodes"]
            owned = sum(
                1 for n in nodes.values()
                if faction and n.get("owner") == faction
            )
            print(f" Nodes owned: {owned}/{len(nodes)}")

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
