def pack(p, jobs=None):
    return {
        "alias": p.get("alias") or "anon",
        "rep": p.get("rep", 0),
        "trace": p.get("trace", 0),
        "jobs": list(jobs or [])[-5:]
    }


def unpack(data, world):
    players = world.get("players")
    if not isinstance(players, dict):
        players = world["players"] = {}

    players[data.get("alias", "anon")] = {
        "rep": data.get("rep", 0),
        "jobs": list(data.get("jobs", []))
    }

    reps = [v.get("rep", 0) for v in players.values()]
    world["rep_avg"] = sum(reps) / len(reps) if reps else 0

    known = world.get("jobs_done")
    known = set(known) if isinstance(known, list) else set()
    world["jobs_done"] = sorted(known | set(data.get("jobs", [])))
