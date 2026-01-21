import time
from core import engine, player
from core.ui import loading

def lay_low():
    if not engine.current_target:
        print("lay-low: no active connection")
        return

    p = player.load()
    trace = p.get("trace", 0)

    if trace <= 0:
        print("lay-low: no trace to reduce")
        return

    print("[STEALTH] dropping off the radar...")
    loading("disabling active channels", 1.5)
    loading("routing traffic through dead drops", 2)

    # reset blue team pressure
    engine.counter_hack = False
    engine.latency = 0.0

    # reduce trace (realistic, not full wipe)
    reduced = min(2, trace)
    p["trace"] -= reduced
    player.save(p)

    print(f"[STEALTH] trace reduced by {reduced}")
    print(f"[STEALTH] current trace: {p['trace']}")

    # optional risk
    if p["trace"] > 5:
        print("[STEALTH] warning: you're still hot")

    # force cooldown
    time.sleep(1)
