import json
import random

DATA = "data"

def load_targets():
    return json.load(open(f"{DATA}/targets.json"))

def generate_notes():
    targets = load_targets()
    keys = list(targets.keys())
    sample = random.sample(keys, min(2, len(keys)))

    lines = ["# personal notes\n"]
    for t in sample:
        os = targets[t]["os"]
        lines.append(f"- heard {t} runs {os}")

    return "\n".join(lines) + "\n"

def generate_leak(target):
    t = load_targets().get(target)
    if not t:
        return "no data"

    return f"""TARGET: {target}
OS: {t['os']}
FIREWALL: {t['firewall']}
VULN SCORE: {t['vuln']}
ONLINE: {t['online']}
"""
