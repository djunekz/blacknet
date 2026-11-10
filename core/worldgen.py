import random

from core import store
from core.paths import DATA


def load_targets():
    data = store.read_json(f"{DATA}/targets.json", {})
    return data if isinstance(data, dict) else {}


def generate_notes():
    targets = load_targets()
    keys = list(targets.keys())
    sample = random.sample(keys, min(2, len(keys)))

    lines = ["# personal notes\n"]
    for t in sample:
        os_name = targets[t].get("os", "unknown")
        lines.append(f"- heard {t} runs {os_name}")

    return "\n".join(lines) + "\n"


def generate_leak(target):
    t = load_targets().get(target)
    if not t:
        return None

    return (
        f"TARGET: {target}\n"
        f"OS: {t.get('os', '?')}\n"
        f"FIREWALL: {t.get('firewall', '?')}\n"
        f"VULN SCORE: {t.get('vuln', '?')}\n"
        f"ONLINE: {t.get('online', '?')}\n"
    )
