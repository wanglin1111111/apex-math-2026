"""Cross-check exact enumeration against brute-force sampling.

This script backs the claim in report.md section 4:
  * 80 equality cross-checks  = 10 configurations x 8 windows, radius 80
  * 240 containment cross-checks = 30 configurations x 8 windows, radius 80

Equality means   exact_patterns(S) == patterns(S, radius)
Containment means exact_patterns(S) >= patterns(S, radius)
i.e. sampling must never find a pattern the exact enumeration missed.

Configurations are drawn from the same generator and seed stream as
run_search.py, so the sample is reproducible.

Usage:
    python code/cross_check.py            # run and write artifacts
    python code/cross_check.py --quiet    # no per-window output
"""

from __future__ import annotations

import argparse
import json
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from run_search import (  # noqa: E402
    DIRECTIONS,
    WINDOWS,
    random_m2,
    targeted_case_b,
)
from star import Experiment2Config  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"

RADIUS = 80
EQUALITY_CONFIGS = 10
CONTAINMENT_CONFIGS = 30
SEED_BASE = 20261027


def sample_configs(n: int, offset: int) -> list[Experiment2Config]:
    """Draw n valid star configurations using run_search.py's seed stream."""
    out: list[Experiment2Config] = []
    cid = offset
    while len(out) < n:
        rng = random.Random(SEED_BASE + cid)
        p = rng.choice([2, 3, 5])
        cfg = targeted_case_b(rng, p) if cid % 5 < 3 else random_m2(rng, p)
        if cfg is None:
            cfg = random_m2(rng, p)
        if not cfg.is_star():
            for _ in range(20):
                cfg = random_m2(rng, p)
                if cfg.is_star():
                    break
            else:
                cid += 1
                continue
        out.append(cfg)
        cid += 1
    return out


def run(n_configs: int, offset: int, mode: str, quiet: bool) -> dict:
    """mode: 'equal' requires set equality, 'contain' only requires >=."""
    configs = sample_configs(n_configs, offset)
    failures: list[dict] = []
    checks = 0
    for idx, cfg in enumerate(configs):
        for wname, S in WINDOWS.items():
            exact = cfg.exact_patterns(S)
            sampled = cfg.patterns(S, radius=RADIUS)
            checks += 1
            ok = (exact == sampled) if mode == "equal" else exact >= sampled
            if not ok:
                failures.append(
                    {
                        "index": idx,
                        "window": wname,
                        "mode": mode,
                        "exact_size": len(exact),
                        "sampled_size": len(sampled),
                        "missed_by_exact": sorted(sampled - exact)[:5],
                    }
                )
            if not quiet:
                flag = "ok" if ok else "MISMATCH"
                print(
                    f"[{mode:<8}] cfg{idx:>2} {wname:<8} "
                    f"|exact|={len(exact):>3} |sampled|={len(sampled):>3} {flag}"
                )
    result = {
        "mode": mode,
        "radius": RADIUS,
        "configs": n_configs,
        "windows": len(WINDOWS),
        "checks": checks,
        "failures": len(failures),
        "failure_detail": failures,
    }
    status = "PASS" if not failures else "FAIL"
    print(
        f"==> {mode}: {checks - len(failures)}/{checks} checks passed "
        f"({n_configs} configs x {len(WINDOWS)} windows, radius {RADIUS}) {status}"
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    eq = run(EQUALITY_CONFIGS, 0, "equal", args.quiet)
    ct = run(CONTAINMENT_CONFIGS, 10000, "contain", args.quiet)

    summary = {
        "radius": RADIUS,
        "equality_cross_checks": {"checks": eq["checks"], "failures": eq["failures"]},
        "containment_cross_checks": {"checks": ct["checks"], "failures": ct["failures"]},
        "total_checks": eq["checks"] + ct["checks"],
        "result": "PASS" if eq["failures"] == 0 and ct["failures"] == 0 else "FAIL",
    }

    ART.mkdir(exist_ok=True)
    path = ART / "cross-check.json"
    path.write_text(json.dumps({"summary": summary, "equality": eq, "containment": ct},
                               indent=1), encoding="utf-8")

    print()
    print(json.dumps(summary, indent=1))
    print("wrote", path)
    return 0 if summary["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
