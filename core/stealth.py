import time

from core import engine, player
from core.ui import loading


def lay_low():
    p = player.load()
    trace = p.get("trace", 0)

    if trace <= 0 and not engine.counter_hack:
        print("lay-low: no trace to reduce")
        return

    print("[STEALTH] dropping off the radar...")
    loading("disabling active channels", 1.5)
    loading("routing traffic through dead drops", 2)

    engine.cool_down()

    reduced = min(2, max(trace, 0))
    p["trace"] = trace - reduced
    player.save(p)

    print(f"[STEALTH] trace reduced by {reduced}")
    print(f"[STEALTH] current trace: {p['trace']}")

    if p["trace"] > 5:
        print("[STEALTH] warning: you're still hot")

    time.sleep(1)
