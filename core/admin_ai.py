import random
from core import engine, player

def patrol():
    p=player.load()

    if p["trace"]>=5:
        if random.random()>0.5:
            print("\n[ADMIN] intrusion detected")
            print("[ADMIN] terminating session\n")
            engine.current_target=None
            engine.logged_user=None
