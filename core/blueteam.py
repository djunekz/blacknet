import random

from core import engine, player
from core.forensics import analyze


def increase_trace(n=1):
    player.add_trace(n)


def counter_hack():
    print("\n[BLUE TEAM] counter intrusion detected")
    engine.counter_hack = True
    engine.latency = random.uniform(0.3, 1.2)


def _tier(score):
    if score >= 9:
        return 3
    if score >= 6:
        return 2
    if score >= 3:
        return 1
    return 0


def respond():
    target = engine.current_target
    if not target:
        return

    score, iocs = analyze()
    tier = _tier(score)

    if tier <= engine.alert_tier.get(target, 0):
        return
    engine.alert_tier[target] = tier

    print("\n[BLUE TEAM] forensic analysis running...")
    for i in iocs:
        print(f"[IOC] {i}")

    if tier == 1:
        print("[BLUE TEAM] alert level: LOW")
        player.add_trace(1)

    elif tier == 2:
        print("[BLUE TEAM] alert level: MEDIUM")
        print("[BLUE TEAM] probing attacker")
        counter_hack()
        player.add_trace(2)

    else:
        print("[BLUE TEAM] alert level: HIGH")
        print("[BLUE TEAM] active incident response engaged")
        counter_hack()
        engine.disconnect()
        player.add_trace(3)
