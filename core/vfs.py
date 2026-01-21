from core import engine
from core.worldgen import generate_notes, generate_leak

# struktur folder virtual
VFS = {
    "/": ["home", "darknet"],
    "/home": ["anon"],
    "/home/anon": ["notes.txt", "leaks"],
    "/home/anon/leaks": [],
    "/darknet": ["bbs.txt"]
}

def list_dir(path):
    return VFS.get(path, [])

def read_file(path):
    if path == "/home/anon/notes.txt":
        return generate_notes()

    if path.startswith("/home/anon/leaks/"):
        target = path.split("/")[-1].replace(".txt", "")
        return generate_leak(target)

    if path == "/darknet/bbs.txt":
        return "The target file is located in the home directory\nOficial Developer : Djunekz (github.com/djunekz/blacknet)"

    return None
