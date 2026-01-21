import random
from core import engine, player
from core.forensics import analyze

# === DIPANGGIL OLEH EXPLOIT / AKSI NOISY ===
def increase_trace(n=1):
    """
    Naikkan trace player secara langsung
    Dipakai oleh exploit, crack, dll
    """
    player.add_trace(n)

# === COUNTER HACK EFFECT ===
def counter_hack():
    print("\n[BLUE TEAM] counter intrusion detected")
    engine.counter_hack = True
    engine.latency = random.uniform(0.3, 1.2)

# === MAIN BLUE TEAM RESPONSE ===
def respond():
    score, iocs = analyze()

    if score == 0:
        return

    print("\n[BLUE TEAM] forensic analysis running...")
    for i in iocs:
        print(f"[IOC] {i}")

    # --- RESPONSE TIERS ---
    if 3 <= score < 6:
        print("[BLUE TEAM] alert level: LOW")
        player.add_trace(1)

    elif 6 <= score < 9:
        print("[BLUE TEAM] alert level: MEDIUM")
        print("[BLUE TEAM] probing attacker")
        counter_hack()
        player.add_trace(2)

    elif score >= 9:
        print("[BLUE TEAM] alert level: HIGH")
        print("[BLUE TEAM] active incident response engaged")
        counter_hack()
        engine.current_target = None
        engine.logged_user = None
        player.add_trace(3)
