from core import engine
from core.vfs import list_dir, read_file
import json

DATA = "data"


def load_target_fs():
    try:
        return json.load(open(f"{DATA}/fs_{engine.current_target}.json"))
    except:
        return {}


# ===== PATH RESOLUTION =====
def resolve(path):
    if path.startswith("/"):
        return path
    if engine.cwd == "/":
        return "/" + path
    return engine.cwd.rstrip("/") + "/" + path


# ===== LS =====
def ls():
    path = engine.cwd

    # PLAYER FS
    if not engine.current_target:
        items = list_dir(path)
        if not items:
            print("not a directory")
        else:
            print("  ".join(items))
        return

    # TARGET FS
    fs = load_target_fs()
    node = fs.get(path)
    if isinstance(node, dict):
        print("  ".join(node.keys()))
    else:
        print("not a directory")


# ===== CD =====
def cd(path=None):
    if not path:
        engine.cwd = "/"
        return

    new = resolve(path)

    # PLAYER FS
    if not engine.current_target:
        if list_dir(new):
            engine.cwd = new
        else:
            print("no such directory")
        return

    # TARGET FS
    fs = load_target_fs()
    if new in fs and isinstance(fs[new], dict):
        engine.cwd = new
    else:
        print("no such directory")


# ===== CAT =====
def cat(path=None):
    if not path:
        print("cat: missing operand")
        return

    full = resolve(path)

    # PLAYER FS
    if not engine.current_target:
        content = read_file(full)
        if content is None:
            print("file not found")
        else:
            print(content)
        return

    # TARGET FS
    fs = load_target_fs()
    if full in fs:
        print(fs[full])
        return

    parent, name = full.rsplit("/", 1)
    parent = parent or "/"
    content = fs.get(parent, {}).get(name)
    if content is not None:
        print(content)
    else:
        print("file not found")
