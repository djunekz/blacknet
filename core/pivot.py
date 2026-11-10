import random

from core import engine, player, logs, store
from core.paths import DATA


def pivot(host):
    if not engine.current_target:
        print("no active session")
        return

    net = store.read_json(f"{DATA}/network_{engine.current_target}.json")
    if not isinstance(net, dict):
        print("network data missing or corrupted")
        return

    nodes = net.get("nodes", {})

    if host not in nodes:
        print("host not reachable")
        return

    if host == engine.current_node:
        print(f"already on {host}")
        return

    node = nodes[host]
    trust = node.get("trust", 3)
    chance = random.randint(1, 5)

    print(f"[*] pivoting to {host}...")

    if chance >= trust:
        logs.write("auth.log", f"lateral access to {host}")
        engine.current_node = host
        engine.cwd = "/"
        engine.logged_user = None
        print("[+] pivot successful")
    else:
        logs.write("auth.log", "pivot failed")
        player.add_trace(2)
        print("[!] pivot failed — anomaly detected")
