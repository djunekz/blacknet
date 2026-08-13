import json, os, random, sys, time

from core import engine
from core.faction import get_faction
from core.netmap import netmap
from core.ui import RED, GREEN, YELLOW, RESET
from core.ids import write
from core.blueteam import increase_trace

DATA = "data"


def load_net():
    if not engine.current_target:
        return None

    path = f"{DATA}/network_{engine.current_target}.json"
    if not os.path.exists(path):
        return None

    try:
        return json.load(open(path))
    except json.JSONDecodeError:
        return None


def save_net(net):
    if not engine.current_target:
        return

    path = f"{DATA}/network_{engine.current_target}.json"
    with open(path, "w") as f:
        json.dump(net, f, indent=2)


def blink_node(node_name, success=True, times=6, delay=0.15):
    color = GREEN if success else RED
    symbol = "✔" if success else "✖"

    for i in range(times):
        dots = "." * (i % 4)
        sys.stdout.write(
            f"\r{color}[WAR] {symbol} contesting {node_name} {dots}{RESET}"
        )
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


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

    if enemy == my:
        print(f"[WAR] {node_name} already controlled by your faction")
        return

    print(f"[WAR] contesting node {node_name}...")

    write(f"faction contest on node {node_name}", "HIGH")

    base = random.randint(1, 10)
    modifier = random.randint(0, 3)
    success = (base + modifier) > 6

    blink_node(node_name, success)

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

    save_net(net)
    netmap()
