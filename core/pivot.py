import json, random
from core import engine, player, logs

DATA = "data"

def pivot(host):
    if not engine.current_target:
        print("no active session")
        return

    path = f"{DATA}/network_{engine.current_target}.json"
    try:
        net = json.load(open(path))
    except (FileNotFoundError, json.JSONDecodeError):
        print("network data missing or corrupted")
        return

    nodes = net.get("nodes", {})

    if host not in nodes:
        print("host not reachable")
        return

    node = nodes[host]
    trust = node.get("trust", 3)
    chance = random.randint(1, 5)

    print(f"[*] pivoting to {host}...")

    if chance >= trust:
        logs.write("auth.log", f"lateral access to {host}")
        engine.current_target = host
        engine.cwd = "/"
        engine.logged_user = None
        print("[+] pivot successful")
    else:
        logs.write("auth.log", "pivot failed")
        player.add_trace(2)
        print("[!] pivot failed — anomaly detected")
