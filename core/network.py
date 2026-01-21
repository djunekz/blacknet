import json, os
from core import engine
from core.ui import BLUE, RED, GREEN, YELLOW, RESET

DATA = "data"

ICON = {
    "router": "📡",
    "subnet": "🗃️",
    "host":   "🖥️"
}

OWNER_COLOR = {
    "red": RED,
    "blue": BLUE,
    "gray": YELLOW,
    None: RESET
}

def netmap():
    if not engine.current_target:
        print("netmap: not connected")
        return

    path = f"{DATA}/network_{engine.current_target}.json"
    if not os.path.exists(path):
        print("netmap: no network data")
        return

    net = json.load(open(path))

    print(f"\n{BLUE}Internal network discovered:{RESET}\n")

    for name, node in net["nodes"].items():
        ntype  = node.get("type", "?")
        status = node.get("status", "unknown")
        owner  = node.get("owner")
        links  = ", ".join(node.get("links", [])) or "-"

        icon  = ICON.get(ntype, "❓")
        color = OWNER_COLOR.get(owner, RESET)

        print(
            f"{color}{icon} {name:<10}"
            f" | type:{ntype:<7}"
            f" | status:{status:<11}"
            f" | owner:{(owner or '-'):>4}"
            f" | links:{links}"
            f"{RESET}"
        )

    print()
