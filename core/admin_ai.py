import random

from core import engine, player


def patrol():
    if not engine.current_target:
        return

    p = player.load()

    if p.get("trace", 0) >= 5 and random.random() > 0.5:
        print("\n[ADMIN] intrusion detected")
        print("[ADMIN] terminating session\n")
        engine.disconnect()
