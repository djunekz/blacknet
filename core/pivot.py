import json, random
from core import engine, player, logs

DATA="data"

def pivot(host):
    if not engine.current_target:
        print("no active session"); return

    net=json.load(open(f"{DATA}/network_{engine.current_target}.json"))

    if host not in net:
        print("host not reachable"); return

    trust=net[host]["trust"]
    chance=random.randint(1,5)

    print(f"[*] pivoting to {host}...")

    if chance >= trust:
        logs.write("auth.log", f"lateral access to {host}")
        engine.current_target=host
        engine.cwd="/"
        engine.logged_user=None
        player.add_trace(0)   # stealth bonus
        print("[+] pivot successful")
    else:
        logs.write("auth.log", "pivot failed")
        player.add_trace(2)
        print("[!] pivot failed — anomaly detected")
