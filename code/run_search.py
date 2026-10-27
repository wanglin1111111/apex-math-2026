"""Run the independent Experiment-2 search for the convex Nivat paper."""

from __future__ import annotations

import csv
import json
import pathlib
import random
import sys
from itertools import product

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from star import (  # noqa: E402
    Experiment2Config,
    convex_hull,
    det,
    dim_us,
    find_d_q,
    h2_rank,
    lattice_points_in_polygon,
    rz_points,
    solve_pi_pair,
    zonotope_lattice_points,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

DIRECTIONS = [
    (1, 0),
    (0, 1),
    (1, 1),
    (1, -1),
    (1, 2),
    (1, -2),
    (2, 1),
    (2, -1),
    (1, 3),
    (1, -3),
    (3, 1),
]


def rect(w: int, h: int) -> list[tuple[int, int]]:
    return [(x, y) for x in range(w) for y in range(h)]


def poly(verts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(lattice_points_in_polygon(convex_hull(verts)))


WINDOWS = {
    "3x4": rect(3, 4),
    "4x4": rect(4, 4),
    "5x3": rect(5, 3),
    "4x3": rect(4, 3),
    "tri15": poly([(0, 0), (4, 0), (0, 4)]),
    "hex17": poly([(1, 0), (3, 0), (4, 2), (3, 4), (1, 4), (0, 2)]),
    "rhomb13": poly([(0, 0), (2, 2), (4, 0), (2, -2)]),
    "para12": poly([(0, 0), (3, 0), (5, 2), (2, 2)]),
}


def targeted_case_b(rng: random.Random, p: int) -> Experiment2Config | None:
    pairs = [(a, b) for a in DIRECTIONS for b in DIRECTIONS if a < b and abs(det(a, b)) >= 2]
    rng.shuffle(pairs)
    for v1, v2 in pairs:
        candidates = []
        for t1 in range(-5, 6):
            for t2 in range(-5, 6):
                if solve_pi_pair(v1, v2, t1, t2) is None:
                    candidates.append((t1, t2))
        if not candidates:
            continue
        t1, t2 = rng.choice(candidates)
        c1, c2 = rng.randrange(p), rng.randrange(p)
        return Experiment2Config(
            p=p,
            directions=[v1, v2],
            constants=[c1, c2],
            windows=[(t1, 1), (t2, 1)],
            values=[[(c1 + 1) % p], [(c2 + 1) % p]],
        )
    return None


def random_m2(rng: random.Random, p: int) -> Experiment2Config:
    dirs = rng.sample(DIRECTIONS, 2)
    constants = [rng.randrange(p), rng.randrange(p)]
    windows = []
    values = []
    for i in range(2):
        length = rng.randint(1, 4)
        start = rng.randint(-3, 3)
        vals = [rng.randrange(p) for _ in range(length)]
        if all(v == constants[i] for v in vals):
            vals[rng.randrange(length)] = (constants[i] + 1) % p
        windows.append((start, length))
        values.append(vals)
    return Experiment2Config(p, dirs, constants, windows, values)


def config_record(cid: int, cfg: Experiment2Config) -> dict:
    return {
        "config_id": cid,
        "p": cfg.p,
        "m": cfg.m,
        "directions": [list(v) for v in cfg.directions],
        "constants": cfg.constants,
        "windows": [list(w) for w in cfg.windows],
        "values": cfg.values,
    }


def main(n_configs: int = 1000, max_rank_checks: int = 60) -> None:
    rows: list[dict] = []
    caseb_rows: list[dict] = []
    validation: list[dict] = []
    violations: list[dict] = []
    configurations: list[dict] = []
    rank_checks = 0
    caseb_rz_pairs = 0

    for cid in range(n_configs):
        rng = random.Random(20261027 + cid)
        p = rng.choice([2, 3, 5])
        cfg = targeted_case_b(rng, p) if cid % 5 < 3 else random_m2(rng, p)
        if cfg is None:
            cfg = random_m2(rng, p)
        if not cfg.is_star():
            # Generate until a valid star configuration; bounded retries.
            for _ in range(20):
                cfg = random_m2(rng, p)
                if cfg.is_star():
                    break
            else:
                continue
        configurations.append(config_record(cid, cfg))
        case = "B" if cfg.case_b_m2() else "A"

        for wname, S in WINDOWS.items():
            pats = cfg.exact_patterns(S)
            P = len(pats)
            bound = len(S) + 1
            holds = P >= bound
            row = {
                "config_id": cid,
                "p": p,
                "case": case,
                "window": wname,
                "size": len(S),
                "Ptheta": P,
                "bound": bound,
                "holds": holds,
                "directions": "|".join(f"{a},{b}" for a, b in cfg.directions),
            }
            rows.append(row)
            if not holds:
                violations.append({**config_record(cid, cfg), **row, "patterns": sorted(pats)})

            if case == "B":
                Zpts = zonotope_lattice_points(cfg.directions, [1] * cfg.m)
                RZ = rz_points(S, cfg.directions, [1] * cfg.m)
                if RZ:
                    caseb_rz_pairs += 1
                    if rank_checks < max_rank_checks:
                        wmap = {a: a + 1 for a in range(cfg.p)}
                        q = 2**31 - 1
                        dim = dim_us(sorted(pats), S, wmap, q)
                        expected_dim = len(S) + 1 - len(RZ)
                        dq = find_d_q(cfg, S, radius=12)
                        h2_val = None
                        expected_h2 = len(S) + 1
                        rank_ok = False
                        d = q0 = None
                        if dq is not None:
                            d, q0 = dq
                            h2_val = h2_rank(cfg, S, sorted(pats), wmap, RZ, d, q0, q)
                            rank_ok = (dim == expected_dim) and (h2_val == expected_h2)
                        caseb_rows.append(
                            {
                                **config_record(cid, cfg),
                                "window": wname,
                                "size": len(S),
                                "Ptheta": P,
                                "RZ_size": len(RZ),
                                "dim_us": dim,
                                "expected_dim": expected_dim,
                                "H2": h2_val,
                                "expected_H2": expected_h2,
                                "d": list(d) if d else None,
                                "q": list(q0) if q0 else None,
                                "rank_ok": rank_ok,
                            }
                        )
                        rank_checks += 1

    summary = {
        "configs_requested": n_configs,
        "configs_generated": len(configurations),
        "window_checks": len(rows),
        "violations": len(violations),
        "case_A": sum(1 for r in rows if r["case"] == "A"),
        "case_B": sum(1 for r in rows if r["case"] == "B"),
        "caseb_rz_pairs": caseb_rz_pairs,
        "rank_checks": rank_checks,
        "rank_ok": sum(1 for r in caseb_rows if r["rank_ok"]),
        "rank_fail": sum(1 for r in caseb_rows if not r["rank_ok"]),
        "windows": {k: len(v) for k, v in WINDOWS.items()},
        "directions": [list(v) for v in DIRECTIONS],
    }

    (ART / "configs.json").write_text(json.dumps(configurations, indent=1), encoding="utf-8")
    (ART / "search-results.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    (ART / "caseb-rank-results.json").write_text(json.dumps(caseb_rows, indent=1), encoding="utf-8")
    (ART / "violations.json").write_text(json.dumps(violations, indent=1), encoding="utf-8")
    (ART / "search-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")

    with (ART / "search-results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    with (ART / "caseb-rank-results.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(caseb_rows[0].keys()) if caseb_rows else ["config_id"])
        writer.writeheader()
        writer.writerows(caseb_rows)

    print(json.dumps(summary, indent=1))
    if violations:
        print("VIOLATIONS", len(violations))
    else:
        print("NO VIOLATIONS")


if __name__ == "__main__":
    main()
