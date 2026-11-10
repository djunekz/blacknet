from core import player, store
from core.jobs import DONE_FILE
from core.net.protocol import pack, unpack
from core.paths import DATA

WORLD = f"{DATA}/world.json"


def load_world():
    world = store.read_json(WORLD)
    if not isinstance(world, dict):
        return {"rep_avg": 0, "jobs_done": []}
    return world


def save_world(w):
    store.write_json(WORLD, w)


def sync():
    world = load_world()
    p = player.load()

    done = store.read_json(DONE_FILE, [])
    ids = [j.get("id") for j in done if isinstance(j, dict) and j.get("id")] if isinstance(done, list) else []

    unpack(pack(p, ids), world)
    save_world(world)
    print("[NET] world state synchronized")
