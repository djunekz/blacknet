import posixpath

from core import engine, store
from core.fs_default import default_fs
from core.paths import DATA
from core.vfs import is_dir, list_dir, read_file


def _is_spec(node, kind):
    return isinstance(node, dict) and node.get("type") == kind


def _subdir(node, name):
    child = node.get(name)
    if not isinstance(child, dict):
        child = node[name] = {}
    return child


def _apply(dirnode, entries):
    if _is_spec(entries, "dir") and isinstance(entries.get("children"), dict):
        entries = entries["children"]

    if isinstance(entries, list):
        for name in entries:
            if isinstance(name, str):
                _subdir(dirnode, name)
        return

    if not isinstance(entries, dict):
        return

    for name, value in entries.items():
        if _is_spec(value, "file"):
            dirnode[name] = str(value.get("content", ""))
        elif isinstance(value, (dict, list)):
            _apply(_subdir(dirnode, name), value)
        elif value is not None:
            dirnode[name] = str(value)


def build_tree(fs):
    tree = {}
    if not isinstance(fs, dict):
        return tree

    for path, entries in fs.items():
        if not isinstance(path, str) or not path.startswith("/"):
            continue
        node = tree
        for part in [p for p in path.split("/") if p]:
            node = _subdir(node, part)
        _apply(node, entries)
    return tree


def load_target_fs():
    if not engine.current_target:
        return None

    raw = store.read_json(f"{DATA}/fs_{engine.current_target}.json", None)
    if raw is None:
        raw = default_fs()
    return build_tree(raw)


def resolve(path):
    if not path.startswith("/"):
        path = posixpath.join(engine.cwd, path)
    return posixpath.normpath(path)


def _walk(tree, path):
    node = tree
    for part in [p for p in path.split("/") if p]:
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def ls(path=None):
    target = resolve(path) if path else engine.cwd

    if not engine.current_target:
        if is_dir(target):
            print("  ".join(list_dir(target)))
        else:
            print("not a directory")
        return

    node = _walk(load_target_fs(), target)
    if isinstance(node, dict):
        print("  ".join(sorted(node.keys())))
    else:
        print("not a directory")


def cd(path=None):
    if not path or path == "/":
        engine.cwd = "/"
        return

    new = resolve(path)

    if not engine.current_target:
        if is_dir(new):
            engine.cwd = new
        else:
            print("no such directory")
        return

    if isinstance(_walk(load_target_fs(), new), dict):
        engine.cwd = new
    else:
        print("no such directory")


def cat(path=None):
    if not path:
        print("cat: missing operand")
        return

    full = resolve(path)

    if not engine.current_target:
        if is_dir(full):
            print("cat: is a directory")
            return
        content = read_file(full)
        if content is None:
            print("file not found")
        else:
            print(content)
        return

    node = _walk(load_target_fs(), full)
    if isinstance(node, dict):
        print("cat: is a directory")
    elif node is None:
        print("file not found")
    else:
        print(node)
