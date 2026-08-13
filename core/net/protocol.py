def pack(p):
    return {
        "rep": p.get("rep", 0),
        "trace": p.get("trace", 0),
        "jobs": p.get("completed_jobs", [])[-5:]
    }

def unpack(data, world):
    world["rep_avg"] += data.get("rep", 0)
    world["jobs_done"].extend(data.get("jobs", []))
