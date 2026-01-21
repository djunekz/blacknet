import json, os
from core import engine
from core.ui import BLUE, RED, GREEN, YELLOW, RESET

DATA="data"

OWNER_COLOR = {
    "red": "\033[31m",
    "blue": "\033[34m",
    "gray": "\033[90m",
    None: "\033[0m"
}

OWNER_ICON = {
    "red": "🟥",
    "blue": "🟦",
    "gray": "⬜",
    None: "  "
}

ICON = {
    "router": "[R]📡",
    "subnet": "[S]🗃️",
    "host":   "[H]🖥️"
}

COLOR = {
    "locked": RED,
    "open": GREEN,
    "compromised": YELLOW,
    "monitored": BLUE
}

def netmap():
    if not engine.current_target:
        print("netmap: not connected to target")
        return

    path = f"{DATA}/network_{engine.current_target}.json"
    if not os.path.exists(path):
        print("netmap: no network data")
        return

    net = json.load(open(path))
    print(f"\nNETWORK MAP :: {net['name']}\n")

    for name, node in net["nodes"].items():
        icon = ICON.get(node.get("type"), "[?]")
        status_color = COLOR.get(node.get("status"), RESET)

        owner = node.get("owner")
        owner_color = OWNER_COLOR.get(owner, RESET)
        owner_icon = OWNER_ICON.get(owner, "  ")

        links = ", ".join(node.get("links", [])) or "-"

        print(
            f"{owner_color}{owner_icon} "
            f"{status_color}{icon} {name:<12} -> {links}"
            f"{RESET}"
        )

    print()
