"""Check submission length, placeholder status, claim traceability and manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def resolve_json(obj, path: str):
    parts = path.replace("[", ".").replace("]", "").split(".")
    cur = obj
    for part in parts:
        if not part:
            continue
        if isinstance(cur, list):
            cur = cur[int(part)]
        else:
            cur = cur[part]
    return cur


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-placeholder", action="store_true")
    parser.add_argument("--check-manifest", action="store_true")
    args = parser.parse_args()

    failures: list[str] = []
    submission = (ROOT / "submission.md").read_text(encoding="utf-8")
    lines = submission.splitlines()
    title = lines[0].lstrip("# ").strip() if lines else ""
    body = "\n".join(lines[1:])
    print(f"title chars: {len(title)} (limit 120)")
    print(f"body chars:  {len(body)} (limit 20000)")
    if len(title) > 120:
        failures.append("title over 120 characters")
    if len(body) > 20000:
        failures.append("body over 20000 characters")
    if "REPO_URL" in submission:
        if args.allow_placeholder:
            print("WARN: REPO_URL placeholder remains (allowed for local pre-push check)")
        else:
            failures.append("REPO_URL placeholder remains")
    if "未逐行人工复核" not in submission:
        failures.append("AI disclosure phrase missing")
    challenge = ROOT / "submission-challenge.md"
    if not challenge.exists() or "不适用" not in challenge.read_text(encoding="utf-8"):
        failures.append("submission-challenge.md missing or not marked 不适用")

    claim_map = ROOT / "report" / "claim-map.csv"
    if not claim_map.exists():
        failures.append("report/claim-map.csv missing")
    else:
        with claim_map.open(encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                artifact = ROOT / row["artifact"]
                if not artifact.exists():
                    failures.append(f"artifact missing: {row['artifact']}")
                    continue
                if row["artifact"].endswith(".json"):
                    data = json.loads(artifact.read_text(encoding="utf-8"))
                    try:
                        value = resolve_json(data, row["path"])
                    except Exception as exc:  # noqa: BLE001
                        failures.append(f"cannot resolve {row['claim']}: {exc}")
                        continue
                    ok = str(value) == row["value"]
                else:
                    text = artifact.read_text(encoding="utf-8")
                    ok = row["path"].removeprefix("text:") in text
                print(f"claim {row['claim']:<18} expected={row['value']:<6} ok={ok}")
                if not ok:
                    failures.append(f"claim mismatch: {row['claim']}")

    manifest = ROOT / "report" / "SHA256SUMS.txt"
    if args.check_manifest and not manifest.exists():
        failures.append("report/SHA256SUMS.txt missing")
    if manifest.exists():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, rel = line.split("  ", 1)
            path = ROOT / rel
            if not path.exists():
                failures.append(f"manifest path missing: {rel}")
                continue
            actual = sha256(path)
            if actual != digest:
                failures.append(f"hash mismatch: {rel}")
        print("manifest entries checked")

    if failures:
        print("\nFAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
