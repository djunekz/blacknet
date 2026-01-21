import json, os, random, sys, time

from core import engine
from core.faction import get_faction
from core.network import netmap
from core.ui import RED, GREEN, YELLOW, RESET
from core.ids import write
from core.blueteam import increase_trace

DATA = "data"

# ===== LOAD / SAVE NETWORK =====
def load_net():
    if not engine.current_target:
        return None

    path = f"{DATA}/network_{engine.current_target}.json"
    if not os.path.exists(path):
        return None

    return json.load(open(path))


def save_net(net):
    if not engine.current_target:
        return

    path = f"{DATA}/network_{engine.current_target}.json"
    json.dump(net, open(path, "w"), indent=2)


# ===== ANIMASI NODE =====
def blink_node(node_name, success=True, times=6, delay=0.15):
    """
    Animasi saat node sedang diperebutkan
    success=True  -> hijau
    success=False -> merah
    """
    color = GREEN if success else RED
    symbol = "✔" if success else "✖"

    for i in range(times):
        dots = "." * (i % 4)
        sys.stdout.write(
            f"\r{color}[WAR] {symbol} contesting {node_name} {dots}{RESET}"
        )
        sys.stdout.flush()
        time.sleep(delay)

    # bersihkan baris
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


# ===== KONTEST NODE =====
def contest(node_name):
    if not engine.current_target:
        print("[WAR] no target connected")
        return

    net = load_net()
    if not net or node_name not in net.get("nodes", {}):
        print(f"[WAR] node '{node_name}' invalid")
        return

    node = net["nodes"][node_name]
    my = get_faction()
    enemy = node.get("owner")

    # ===== ALREADY OWNED =====
    if enemy == my:
        print(f"[WAR] {node_name} already controlled by your faction")
        return

    print(f"[WAR] contesting node {node_name}...")

    # IDS: aksi sangat noisy
    write(f"faction contest on node {node_name}", "HIGH")

    # ===== RANDOM CHANCE =====
    base = random.randint(1, 10)
    modifier = random.randint(0, 3)
    success = (base + modifier) > 6

    # ===== ANIMASI =====
    blink_node(node_name, success)

    # ===== HASIL =====
    if success:
        node["owner"] = my
        node["status"] = "compromised"
        write(f"node {node_name} captured by {my}", "HIGH")
        print(f"{GREEN}[WAR] node {node_name} captured by {my.upper()}{RESET}")

    else:
        node["status"] = "monitored"
        write(f"failed contest on node {node_name}", "MEDIUM")
        increase_trace(2)
        print(
            f"{RED}[WAR] contest failed — node {node_name} under monitoring{RESET}"
        )

    # ===== SIMPAN & TAMPILKAN =====
    save_net(net)
    netmap()
