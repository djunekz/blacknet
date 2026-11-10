import posixpath

from core.worldgen import generate_notes, generate_leak, load_targets

LEAKS = "/home/anon/leaks"

VFS = {
    "/": ["home", "darknet"],
    "/home": ["anon"],
    "/home/anon": ["notes.txt", "leaks"],
    "/darknet": ["bbs.txt"]
}


def is_dir(path):
    return path in VFS or path == LEAKS


def list_dir(path):
    if path == LEAKS:
        return [f"{t}.txt" for t in sorted(load_targets())]
    return VFS.get(path, [])


def read_file(path):
    if path == "/home/anon/notes.txt":
        return generate_notes()

    if posixpath.dirname(path) == LEAKS:
        target = posixpath.basename(path)
        if target.endswith(".txt"):
            target = target[:-4]
        return generate_leak(target)

    if path == "/darknet/bbs.txt":
        return "The target file is located in the home directory\nOfficial Developer : Djunekz (github.com/djunekz/blacknet)"

    return None
