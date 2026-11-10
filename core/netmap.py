from core import engine, store
from core.paths import DATA
from core.ui import BLUE, RED, GREEN, YELLOW, RESET

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

    net = store.read_json(f"{DATA}/network_{engine.current_target}.json")
    if net is None:
        print("netmap: no network data")
        return

    if not isinstance(net, dict) or not isinstance(net.get("nodes"), dict):
        print("netmap: network data corrupted")
        return

    print(f"\nNETWORK MAP :: {net.get('name', engine.current_target)}\n")

    for name, node in net["nodes"].items():
        icon = ICON.get(node.get("type"), "[?]")
        status_color = COLOR.get(node.get("status"), RESET)

        owner = node.get("owner")
        owner_color = OWNER_COLOR.get(owner, RESET)
        owner_icon = OWNER_ICON.get(owner, "  ")

        links = ", ".join(node.get("links", [])) or "-"
        here = "*" if name == engine.current_node else " "

        print(
            f"{owner_color}{owner_icon} "
            f"{status_color}{here}{icon} {name:<12} -> {links}"
            f"{RESET}"
        )

    print()
