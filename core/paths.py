import os
import shutil

from core.version import __version__

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_DIR = os.path.join(BASE_DIR, "data")

RUNTIME_PREFIXES = (
    "player",
    "profile",
    "world",
    "logs_",
    "persist_",
    "creds_",
    "jobs_taken",
    "jobs_done",
    "ids.log",
    ".seed_version",
)

STATIC_PREFIXES = ("jobs.json", "targets.json", "wordlist.txt", "users_", "fs_")


def is_android():
    return "ANDROID_ARGUMENT" in os.environ or "ANDROID_PRIVATE" in os.environ


def data_dir():
    override = os.environ.get("BLACKNET_HOME")
    if override:
        return os.path.join(os.path.abspath(os.path.expanduser(override)), "data")
    if is_android():
        root = os.environ.get("ANDROID_PRIVATE") or BASE_DIR
        return os.path.join(root, "blacknet", "data")
    return SEED_DIR


DATA = data_dir()


def ensure_data():
    os.makedirs(DATA, exist_ok=True)
    if os.path.abspath(DATA) == os.path.abspath(SEED_DIR) or not os.path.isdir(SEED_DIR):
        return

    stamp = os.path.join(DATA, ".seed_version")
    try:
        with open(stamp, encoding="utf-8") as f:
            current = f.read().strip()
    except OSError:
        current = ""
    upgraded = current != __version__

    for name in sorted(os.listdir(SEED_DIR)):
        src = os.path.join(SEED_DIR, name)
        if not os.path.isfile(src) or name.startswith(RUNTIME_PREFIXES):
            continue
        dst = os.path.join(DATA, name)
        if not os.path.exists(dst) or (upgraded and name.startswith(STATIC_PREFIXES)):
            shutil.copyfile(src, dst)

    with open(stamp, "w", encoding="utf-8") as f:
        f.write(__version__)
