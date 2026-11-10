import argparse
import sys
import time

from core import engine, player
from core.admin_ai import patrol
from core.apropos import apropos
from core.auth import ssh
from core.blueteam import respond
from core.crack import crack
from core.exploit import exploit
from core.faction import choose_faction, get_faction
from core.filesystem import cat, cd, ls
from core.help import show_help
from core.ids import clear as ids_clear
from core.ids import read as ids_read
from core.jobs import complete, list_jobs, take
from core.man import man
from core.net.github_sync import pull_world, push_report
from core.net.sync import sync
from core.netmap import netmap
from core.paths import ensure_data
from core.persistence import (
    install_backdoor,
    install_cron,
    install_service,
    reconnect
)
from core.pivot import pivot
from core.privilage import sudo
from core.stealth import lay_low
from core.status import status
from core.ui import banner, counter_warning, loading, splash, status_bar
from core.version import __version__
from core.war import contest


def _persist(sub=None):
    actions = {
        "backdoor": install_backdoor,
        "cron": install_cron,
        "service": install_service
    }
    action = actions.get(sub)
    if action is None:
        print("usage: persist [backdoor|cron|service]")
        return
    action()


def _pull():
    world = pull_world()
    if world:
        print("[WORLD SYNCED]")
        print(world)


COMMANDS = {
    "exploit": (exploit, 1, 1, "exploit <target>"),
    "ls": (ls, 0, 1, "ls [path]"),
    "cd": (cd, 0, 1, "cd [dir]"),
    "cat": (cat, 1, 1, "cat <file>"),
    "ssh": (ssh, 1, 1, "ssh <user>"),
    "crack": (crack, 2, 2, "crack <target> <user>"),
    "sudo": (sudo, 1, 1, "sudo <password>"),
    "netmap": (netmap, 0, 0, "netmap"),
    "pivot": (pivot, 1, 1, "pivot <node>"),
    "help": (show_help, 0, 1, "help [topic]"),
    "man": (man, 1, 1, "man <command>"),
    "apropos": (apropos, 1, 1, "apropos <keyword>"),
    "status": (status, 0, 0, "status"),
    "persist": (_persist, 1, 1, "persist [backdoor|cron|service]"),
    "reconnect": (reconnect, 0, 1, "reconnect [target]"),
    "jobs": (list_jobs, 0, 0, "jobs"),
    "take": (take, 1, 1, "take <job_id>"),
    "complete": (complete, 1, 1, "complete <job_id>"),
    "sync": (sync, 0, 0, "sync"),
    "pull": (_pull, 0, 0, "pull"),
    "push": (push_report, 0, 0, "push"),
    "contest": (contest, 1, 1, "contest <node>"),
    "lay-low": (lay_low, 0, 0, "lay-low"),
    "ids": (ids_read, 0, 0, "ids"),
    "ids-clear": (ids_clear, 0, 0, "ids-clear"),
}


def run_command(name, args):
    entry = COMMANDS.get(name)
    if entry is None:
        print("command not found")
        return

    handler, low, high, usage = entry
    if not low <= len(args) <= high:
        print(f"usage: {usage}")
        return

    try:
        handler(*args)
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[!] internal error in '{name}': {type(e).__name__}: {e}")


def _confirm_exit():
    try:
        ans = input("\nDo you really want to exit the game? [Y/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return True
    return ans in ("y", "yes", "")


def _clean_alias(text):
    text = "".join(ch for ch in text if ch.isprintable()).strip()
    return text[:24] or "anon"


def _setup():
    banner()

    p = player.load()
    if not p.get("alias"):
        p["alias"] = _clean_alias(input("Choose your alias: "))
        player.save(p)

    faction = get_faction() or choose_faction()
    if not faction:
        return False

    splash(faction)
    loading("establishing secure channel", 1.5)
    loading("connecting to darknet", 3)
    return True


def _setup_with_resume():
    while True:
        try:
            return _setup()
        except KeyboardInterrupt:
            if _confirm_exit():
                print("[EXIT] Session terminated.")
                return False
            print("[RESUME TO GAME]")


def _prompt(p):
    who = engine.logged_user or p.get("alias") or "shell"
    tgt = engine.current_target or "local"
    if engine.current_node:
        tgt = f"{tgt}/{engine.current_node}"
    return f"{who}@{tgt}:{engine.cwd}$ "


def _loop():
    while True:
        try:
            p = player.load()
            status_bar(engine, p)

            if engine.counter_hack:
                counter_warning()
                time.sleep(engine.latency or 0.7)

            parts = input(_prompt(p)).strip().split()
            if not parts:
                continue

            name, args = parts[0].lower(), parts[1:]

            if name == "exit":
                print("[EXIT] Goodbye.")
                return

            run_command(name, args)

            patrol()
            respond()

        except KeyboardInterrupt:
            if _confirm_exit():
                print("[EXIT] Session terminated.")
                return
            print("[RESUME]")


def run():
    ensure_data()
    try:
        if not _setup_with_resume():
            return 0
        _loop()
    except EOFError:
        print("\n[EXIT] input closed.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="blacknet",
        description="BLACKNET terminal hacking simulation"
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"blacknet {__version__}"
    )
    parser.parse_args(argv)
    return run()


if __name__ == "__main__":
    sys.exit(main())
