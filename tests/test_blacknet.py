import builtins
import contextlib
import io
import json
import os
import random
import shutil
import sys
import tempfile
import time
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

HOME = tempfile.mkdtemp(prefix="blacknet-test-")
os.environ["BLACKNET_HOME"] = HOME
os.environ["BLACKNET_FAST"] = "1"

from core import engine, paths, player
from core.ansi import Screen, parse_status
from core.bridge import Bridge


def reset():
    shutil.rmtree(paths.DATA, ignore_errors=True)
    paths.ensure_data()
    engine.disconnect()
    engine.cool_down()
    engine.last_target = None
    engine.alert_tier.clear()
    player.save(dict(player.DEFAULT, alias="tester"))


def capture(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args)
    return buf.getvalue()


def run_session(commands):
    feed = iter(commands)

    def fake_input(prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError

    from core import game
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), \
            mock.patch.object(builtins, "input", fake_input), \
            mock.patch.object(time, "sleep", lambda *_: None), \
            mock.patch.object(random, "random", lambda: 0.3), \
            mock.patch.object(random, "randint", lambda a, b: b):
        game.run()
    return buf.getvalue()


class BaseCase(unittest.TestCase):
    def setUp(self):
        reset()
        patcher = mock.patch.object(time, "sleep", lambda *_: None)
        patcher.start()
        self.addCleanup(patcher.stop)

    @classmethod
    def tearDownClass(cls):
        pass


class FilesystemTests(BaseCase):
    def test_target_root_listing_and_navigation(self):
        from core.filesystem import cat, cd, ls
        engine.connect("gov-id-01")
        self.assertEqual(capture(ls).split(), ["etc", "home", "var"])
        cd("/var/log")
        self.assertEqual(engine.cwd, "/var/log")
        self.assertIn("auth.log", capture(ls))
        cd("..")
        self.assertEqual(engine.cwd, "/var")
        self.assertIn("ssh login failed", capture(cat, "/var/log/auth.log"))

    def test_default_fs_for_unknown_target(self):
        from core.filesystem import cat, ls
        engine.connect("bank-neo")
        self.assertEqual(capture(ls).split(), ["etc", "home", "var"])
        self.assertIn("root:x:0:0", capture(cat, "/etc/passwd"))

    def test_spec_format_is_supported(self):
        from core.filesystem import build_tree
        tree = build_tree({"/": {"type": "dir", "children": {
            "etc": {"type": "dir", "children": {
                "passwd": {"type": "file", "content": "root:x:0:0"}}}}}})
        self.assertEqual(tree["etc"]["passwd"], "root:x:0:0")

    def test_local_vfs_leaks_directory(self):
        from core.filesystem import cat, cd, ls
        cd("/home/anon/leaks")
        self.assertEqual(engine.cwd, "/home/anon/leaks")
        self.assertIn("gov-id-01.txt", capture(ls))
        self.assertIn("TARGET: gov-id-01", capture(cat, "gov-id-01.txt"))
        self.assertIn("file not found", capture(cat, "missing.txt"))


class AuthTests(BaseCase):
    def test_admin_password_is_crackable_and_sudo_works(self):
        from core.auth import ssh
        from core.crack import crack
        from core.privilage import sudo
        engine.connect("gov-id-01")
        self.assertIn("PASSWORD FOUND", capture(crack, "gov-id-01", "admin"))
        self.assertIn("logged in as admin", capture(ssh, "admin"))
        self.assertIn("root shell granted", capture(sudo, "toor"))
        self.assertEqual(engine.logged_user, "root")

    def test_crack_rejects_path_traversal(self):
        from core.crack import crack
        self.assertIn("invalid target", capture(crack, "../../etc/x", "root"))
        self.assertIn("invalid target", capture(crack, "a/b", "root"))


class BlueTeamTests(BaseCase):
    def test_response_is_not_repeated_every_command(self):
        from core import ids
        from core.blueteam import respond
        engine.connect("gov-id-01")
        ids.write("exploit chain initiated", "HIGH")
        ids.write("shell access obtained", "HIGH")
        for _ in range(6):
            capture(respond)
        self.assertEqual(player.load()["trace"], 1)

    def test_fresh_logs_do_not_look_wiped(self):
        from core.forensics import analyze
        from core.logs import init_logs
        engine.connect("gov-id-01")
        init_logs()
        score, iocs = analyze()
        self.assertEqual(score, 0)
        self.assertNotIn("auth log wiped", iocs)

    def test_cleared_log_is_flagged_as_wiped(self):
        from core import logs
        from core.forensics import analyze
        engine.connect("gov-id-01")
        logs.write("auth.log", "something")
        capture(logs.clear, "auth.log")
        self.assertIn("auth log wiped", analyze()[1])

    def test_patrol_is_silent_when_offline(self):
        from core.admin_ai import patrol
        p = player.load()
        p["trace"] = 9
        player.save(p)
        with mock.patch.object(random, "random", lambda: 0.99):
            self.assertEqual(capture(patrol), "")

    def test_disconnect_resets_cwd(self):
        engine.connect("gov-id-01")
        engine.cwd = "/etc"
        engine.disconnect()
        self.assertEqual(engine.cwd, "/")
        self.assertIsNone(engine.current_target)

    def test_lay_low_works_offline_and_clears_counter_hack(self):
        from core.stealth import lay_low
        p = player.load()
        p["trace"] = 4
        player.save(p)
        engine.counter_hack = True
        capture(lay_low)
        self.assertFalse(engine.counter_hack)
        self.assertEqual(player.load()["trace"], 2)


class NetworkTests(BaseCase):
    def test_pivot_changes_node_not_target(self):
        from core.pivot import pivot
        engine.connect("gov-id-01")
        with mock.patch.object(random, "randint", lambda a, b: 5):
            capture(pivot, "internal-db")
        self.assertEqual(engine.current_target, "gov-id-01")
        self.assertEqual(engine.current_node, "internal-db")

    def test_netmap_marks_current_node(self):
        from core.netmap import netmap
        engine.connect("gov-id-01")
        engine.current_node = "dmz"
        out = capture(netmap)
        self.assertIn("*", out)
        self.assertIn("internal-db", out)

    def test_contest_requires_faction(self):
        from core.war import contest
        engine.connect("gov-id-01")
        self.assertIn("choose a faction", capture(contest, "gateway"))


class PersistenceTests(BaseCase):
    def test_reconnect_after_disconnect(self):
        from core.persistence import install_backdoor, reconnect
        engine.connect("gov-id-01")
        engine.logged_user = "root"
        capture(install_backdoor)
        engine.disconnect()
        out = capture(reconnect)
        self.assertIn("reconnected", out)
        self.assertEqual(engine.current_target, "gov-id-01")

    def test_reconnect_without_history(self):
        from core.persistence import reconnect
        self.assertIn("no previous target", capture(reconnect))


class JobTests(BaseCase):
    def test_take_and_complete_is_case_insensitive_and_pays_once(self):
        from core.jobs import complete, take
        capture(take, "job-004")
        capture(complete, "JOB-004")
        capture(complete, "JOB-004")
        p = player.load()
        self.assertEqual(p["credits"], 600)
        self.assertEqual(p["rep"], 4)

    def test_reward_dict_format_from_spec(self):
        from core import jobs
        with open(jobs.JOBS_FILE, "w", encoding="utf-8") as f:
            json.dump([{"id": "JOB-X", "title": "t", "reward": {"credits": 70, "rep": 3}}], f)
        out = capture(jobs.list_jobs)
        self.assertIn("70 credits", out)
        capture(jobs.take, "JOB-X")
        capture(jobs.complete, "JOB-X")
        self.assertEqual(player.load()["credits"], 170)

    def test_sync_is_idempotent(self):
        from core.net.sync import load_world, sync
        capture(sync)
        first = load_world()
        capture(sync)
        capture(sync)
        self.assertEqual(load_world(), first)


class StorageTests(BaseCase):
    def test_corrupt_player_file_recovers(self):
        with open(player.PLAYER, "w", encoding="utf-8") as f:
            f.write("{not json")
        self.assertEqual(player.load()["credits"], 100)

    def test_seed_upgrade_keeps_runtime_state(self):
        net = os.path.join(paths.DATA, "network_gov-id-01.json")
        with open(net, "w", encoding="utf-8") as f:
            f.write('{"name": "mine", "nodes": {}}')
        with open(os.path.join(paths.DATA, ".seed_version"), "w", encoding="utf-8") as f:
            f.write("0.0.1")
        with open(os.path.join(paths.DATA, "wordlist.txt"), "w", encoding="utf-8") as f:
            f.write("old\n")
        paths.ensure_data()
        with open(net, encoding="utf-8") as f:
            self.assertIn("mine", f.read())
        with open(os.path.join(paths.DATA, "wordlist.txt"), encoding="utf-8") as f:
            self.assertIn("admin123", f.read())


class AndroidLayerTests(unittest.TestCase):
    def test_screen_handles_cr_clear_and_split_escape(self):
        s = Screen(cols=20)
        s.feed("loading |\rloading /\rdone      \n")
        s.feed("\x1b[3")
        s.feed("1mred\x1b[0m\n")
        self.assertEqual(s.plain_lines()[:2], ["done      ", "red"])
        self.assertIn("[color=#ff6b7a]red[/color]", s.markup_lines()[1])
        s.feed("\x1b[2J\x1b[3J\x1b[Hnew")
        self.assertEqual(s.plain_lines(), ["new"])

    def test_screen_wraps_and_escapes_markup(self):
        s = Screen(cols=5)
        s.feed("abcdefgh\n[x]\n")
        self.assertEqual(s.plain_lines()[:3], ["abcde", "fgh", "[x]"])
        self.assertEqual(s.markup_lines()[2], "&bl;x&br;")

    def test_emoji_fallback_in_markup(self):
        s = Screen()
        s.feed("🟥 📡")
        self.assertNotIn("🟥", s.markup_lines()[0])

    def test_parse_status_reads_hud_values(self):
        s = Screen(cols=80)
        s.feed("\x1b[34m[TARGET:gov-id-01]\x1b[36m [NODE:n2]\x1b[33m [TRACE:42]\x1b[32m [REP:-3]\x1b[0m\n")
        self.assertEqual(parse_status(s.plain_lines()), ("gov-id-01", 42, -3))
        self.assertIsNone(parse_status(["nothing here"]))

    def test_compact_banner_has_no_block_art(self):
        from core import ui
        with mock.patch.dict(os.environ, {"BLACKNET_COMPACT": "1", "BLACKNET_FAST": "1"}):
            out = capture(ui.banner)
            splash = capture(ui.splash, "red")
        self.assertIn("B L A C K N E T", out)
        self.assertNotIn("\u2588", out)
        self.assertIn("RED HAT", splash)
        self.assertNotIn("\u2588", splash)

    def test_bridge_roundtrip_and_close(self):
        b = Bridge()
        b.submit("hello")
        self.assertEqual(b.input("> "), "hello")
        out = b.drain()
        self.assertIn("hello\n", out)
        self.assertIn("> ", out)
        b.close()
        with self.assertRaises(EOFError):
            b.input("> ")


class GameSessionTests(BaseCase):
    def test_full_session(self):
        out = run_session([
            "tester", "red",
            "exploit gov-id-01", "ids-clear",
            "crack gov-id-01 root", "ssh root",
            "persist backdoor", "ls", "cd /etc", "cat passwd", "cd ..",
            "netmap", "jobs", "take job-002", "complete JOB-002",
            "exploit", "LS", "bogus", "exit",
        ])
        for needle in (
            "shell access granted",
            "logged in as root",
            "backdoor installed",
            "etc  home  var",
            "root:x:0:0",
            "NETWORK MAP",
            "usage: exploit <target>",
            "command not found",
            "[EXIT] Goodbye.",
        ):
            self.assertIn(needle, out)
        self.assertEqual(player.load()["credits"], 300)

    def test_eof_exits_cleanly(self):
        out = run_session(["tester", "gray"])
        self.assertIn("input closed", out)

    def test_aborted_faction_selection_exits(self):
        from core import game
        with mock.patch.object(game, "choose_faction", lambda: None):
            out = run_session(["tester"])
        self.assertNotIn("Traceback", out)

    def test_version_flag(self):
        from core import game
        with self.assertRaises(SystemExit) as ctx:
            capture(game.main, ["--version"])
        self.assertEqual(ctx.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
