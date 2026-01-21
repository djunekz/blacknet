def pack(player):
    return {
        "rep": player.rep,
        "trace": player.trace,
        "jobs": player.completed_jobs[-5:]
    }

def unpack(data, world):
    world["rep_avg"] += data.get("rep", 0)
    world["jobs_done"].extend(data.get("jobs", []))
