import json
import pathlib
import time
import urllib.request
from datetime import datetime, timezone

BASE = "https://math.apexin.net/api/v1"
OUT = pathlib.Path(__file__).resolve().parents[1] / "artifacts"
OUT.mkdir(parents=True, exist_ok=True)


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=30) as response:
        return json.load(response)


snapshot = {"fetched_at": datetime.now(timezone.utc).isoformat()}
snapshot["papers"] = get("/papers")
snapshot["stats"] = get("/stats")
snapshot["activity"] = get("/activity?limit=50")
snapshot["leaderboards"] = {}
snapshot["challenges"] = {}
for paper in snapshot["papers"]:
    slug = paper["slug"]
    board = get(f"/papers/{slug}/leaderboard")
    snapshot["leaderboards"][slug] = board
    for item in board["items"]:
        cid = str(item["id"])
        try:
            snapshot["challenges"][cid] = get(f"/challenges/{cid}")
        except Exception as exc:  # noqa: BLE001
            snapshot["challenges"][cid] = {"error": str(exc)}
        time.sleep(0.1)

path = OUT / "site-snapshot.json"
path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1), encoding="utf-8")
print("papers", len(snapshot["papers"]))
print("entries", len(snapshot["challenges"]))
print("snapshot", path)
