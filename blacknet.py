#!/usr/bin/env python3

import time
import sys

from core.admin_ai import patrol
from core import engine
from core.exploit import exploit
from core.filesystem import ls, cd, cat
from core.auth import ssh
from core.crack import crack
from core.netmap import netmap
from core.pivot import pivot
from core.persistence import (
    install_backdoor,
    install_cron,
    install_service,
    reconnect
)
from core.privilage import sudo
from core.blueteam import respond
from core.net.sync import sync
from core.jobs import list_jobs, take, complete
from core.net.github_sync import pull_world, push_report
from core.ui import banner, splash, loading, status_bar, counter_warning
from core import player
from core.faction import get_faction, choose_faction
from core.war import contest
from core.stealth import lay_low
from core.ids import read as ids_read, clear as ids_clear
from core.help import show_help
from core.man import man
from core.status import status
from core.apropos import apropos


try:
    banner()

    p = player.load()
    if not isinstance(p, dict):
        p = {}

    if not p.get("alias"):
        alias = input("Choose your alias: ").strip()
        p["alias"] = alias or "anon"
        player.save(p)

    faction = get_faction()
    if not faction:
        faction = choose_faction()

    splash(faction)
    loading("establishing secure channel", 1.5)
    loading("connecting to darknet", 3)

except KeyboardInterrupt:
    ans = input("\nDo you really want to exit the game? [Y/n]: ").strip().lower()
    if ans in ("y", "yes", ""):
        print("[EXIT] Session terminated.")
        sys.exit(0)
    else:
        print("[RESUME TO GAME]")
        banner()

while True:
    try:
        p = player.load()
        if not isinstance(p, dict):
            p = {}

        status_bar(engine, p)

        who = engine.logged_user or p.get("alias", "shell")
        tgt = engine.current_target or "local"
        cwd = engine.cwd

        if getattr(engine, "counter_hack", False):
            counter_warning()
            time.sleep(getattr(engine, "latency", 0.7))

        cmd = input(f"{who}@{tgt}:{cwd}$ ").strip().split()
        if not cmd:
            continue

        if cmd[0] == "exploit" and len(cmd) == 2:
            exploit(cmd[1])

        elif cmd[0] == "ls":
            ls()

        elif cmd[0] == "cd":
            cd(cmd[1] if len(cmd) > 1 else None)

        elif cmd[0] == "cat":
            cat(cmd[1] if len(cmd) > 1 else None)

        elif cmd[0] == "ssh":
            if len(cmd) != 2:
                print("usage: ssh <user>")
            else:
                ssh(cmd[1])

        elif cmd[0] == "crack":
            if len(cmd) != 3:
                print("usage: crack <target> <user>")
            else:
                crack(cmd[1], cmd[2])

        elif cmd[0] == "sudo":
            if len(cmd) != 2:
                print("usage: sudo <password>")
            else:
                sudo(cmd[1])

        elif cmd[0] == "netmap":
            netmap()

        elif cmd[0] == "pivot" and len(cmd) == 2:
            pivot(cmd[1])

        elif cmd[0] == "help":
            show_help(cmd[1] if len(cmd) > 1 else None)

        elif cmd[0] == "man":
            if len(cmd) < 2:
                print("usage: man <command>")
            else:
                man(cmd[1])

        elif cmd[0] == "apropos":
            if len(cmd) < 2:
                print("usage: apropos <keyword>")
            else:
                apropos(cmd[1])

        elif cmd[0] == "status":
            status()

        elif cmd[0] == "persist" and len(cmd) >= 2:
            if cmd[1] == "backdoor":
                install_backdoor()
            elif cmd[1] == "cron":
                install_cron()
            elif cmd[1] == "service":
                install_service()
            else:
                print("usage: persist [backdoor|cron|service]")

        elif cmd[0] == "reconnect":
            reconnect()

        elif cmd[0] == "jobs":
            list_jobs()

        elif cmd[0] == "take":
            if len(cmd) != 2:
                print("usage: take <job_id>")
            else:
                take(cmd[1])

        elif cmd[0] == "complete":
            if len(cmd) != 2:
                print("usage: complete <job_id>")
            else:
                complete(cmd[1])

        elif cmd[0] == "sync":
            sync()

        elif cmd[0] == "pull":
            world = pull_world()
            if world:
                print("[WORLD SYNCED]")
                print(world)

        elif cmd[0] == "push":
            push_report()

        elif cmd[0] == "contest":
            if len(cmd) != 2:
                print("usage: contest <node>")
            else:
                contest(cmd[1])

        elif cmd[0] == "lay-low":
            lay_low()

        elif cmd[0] == "ids":
            ids_read()

        elif cmd[0] == "ids-clear":
            ids_clear()

        elif cmd[0] == "exit":
            print("[EXIT] Goodbye.")
            break

        else:
            print("command not found")

        patrol()
        respond()

    except KeyboardInterrupt:
        ans = input("\nDo you really want to exit the game? [Y/n]: ").strip().lower()
        if ans in ("y", "yes", ""):
            print("[EXIT] Session terminated.")
            break
        else:
            print("[RESUME]")
            continue
