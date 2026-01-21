import os, sys, time
from core import player

# ===== ANSI COLORS =====
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
RESET  = "\033[0m"
GREY   = "\033[90m"
BOLD   = "\033[1m"

def clear():
    os.system("clear")

def slow_print(text, delay=0.01):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def banner():
    clear()
    print(CYAN + BOLD)
    print(r"""
██████╗ ██╗      █████╗  ██████╗██╗  ██╗███╗   ██╗███████╗████████╗
██╔══██╗██║     ██╔══██╗██╔════╝██║ ██╔╝████╗  ██║██╔════╝╚══██╔══╝
██████╔╝██║     ███████║██║     █████╔╝ ██╔██╗ ██║█████╗     ██║
██╔══██╗██║     ██╔══██║██║     ██╔═██╗ ██║╚██╗██║██╔══╝     ██║
██████╔╝███████╗██║  ██║╚██████╗██║  ██╗██║ ╚████║███████╗   ██║
╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝
    """)
    print(RESET)
    slow_print(":: BLACKNET underground access established ::", 0.02)
    print()

def loading(text="connecting", t=1.5, done="done"):
    frames = ["|", "/", "-", "\\"]
    end = time.time() + t
    i = 0

    while time.time() < end:
        sys.stdout.write(f"\r{text} {frames[i % len(frames)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")
    sys.stdout.flush()

    if done:
        print(f"[+] {text} {done}")

def status_bar(engine, _player_module):
    p = player.load()  # ambil data player dari file

    trace = p.get("trace", 0)
    rep   = p.get("rep", 0)

    print(
        BLUE   + f"[TARGET:{engine.current_target or 'LOCAL'}]"
        + YELLOW + f" [TRACE:{trace}]"
        + GREEN  + f" [REP:{rep}]"
        + RESET
    )

def splash(faction):
    clear()
    print(BOLD)
    if faction == "red":
        print(RED + r"""
 ██████╗ ███████╗██████╗
 ██╔══██╗██╔════╝██╔══██╗
 ██████╔╝█████╗  ██║  ██║
 ██╔══██╗██╔══╝  ██║  ██║
 ██║  ██║███████╗██████╔╝
 ╚═╝  ╚═╝╚══════╝╚═════╝
""")
        slow_print(":: RED Hat Hacker — strike first, vanish fast ::", 0.02)

    elif faction == "blue":
        print(BLUE + r"""
 ██████╗ ██╗     ██╗   ██╗███████╗
 ██╔══██╗██║     ██║   ██║██╔════╝
 ██████╔╝██║     ██║   ██║█████╗
 ██╔══██╗██║     ██║   ██║██╔══╝
 ██████╔╝███████╗╚██████╔╝███████╗
 ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝
""")
        slow_print(":: BLUE Hat Hacker — detect, contain, respond ::", 0.02)

    else:
        print(GREY + r"""
  ██████╗ ██████╗  █████╗ ██╗   ██╗
 ██╔════╝ ██╔══██╗██╔══██╗╚██╗ ██╔╝
 ██║  ███╗██████╔╝███████║ ╚████╔╝
 ██║   ██║██╔══██╗██╔══██║  ╚██╔╝
 ╚██████╔╝██║  ██║██║  ██║   ██║
  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
""")
        slow_print(":: GRAY Hat Hacker — profit over ideology ::", 0.02)

    print(RESET)

def counter_warning():
    print("\033[31m[!] incoming counter-hack traffic detected\033[0m")
