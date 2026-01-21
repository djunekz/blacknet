import json, os
from core.net.protocol import pack, unpack
from core import player

WORLD="data/world.json"

def load_world():
    if not os.path.exists(WORLD):
        return {"rep_avg":0,"jobs_done":[]}
    return json.load(open(WORLD))

def save_world(w):
    json.dump(w, open(WORLD,"w"), indent=2)

def sync():
    world = load_world()
    data = pack(player)
    unpack(data, world)
    save_world(world)
    print("[NET] world state synchronized")
