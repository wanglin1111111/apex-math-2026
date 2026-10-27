"""Reproduce the two representative rows of Appendix C.2 and save the evidence."""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from star import (  # noqa: E402
    Experiment2Config,
    convex_hull,
    dim_us,
    find_d_q,
    h2_rank,
    lattice_points_in_polygon,
    rz_points,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"


def poly(verts):
    return sorted(lattice_points_in_polygon(convex_hull(verts)))


def row(cfg: Experiment2Config, name: str, S, expected: dict) -> dict:
    pats = sorted(cfg.exact_patterns(S))
    RZ = rz_points(S, cfg.directions, [1] * cfg.m)
    w = {a: a + 1 for a in range(cfg.p)}
    q = 2**31 - 1
    dim = dim_us(pats, S, w, q)
    dq = find_d_q(cfg, S, radius=12)
    if dq is None:
        raise RuntimeError("no witness d")
    d, q0 = dq
    h2 = h2_rank(cfg, S, pats, w, RZ, d, q0, q)
    got = {
        "window": name,
        "size": len(S),
        "Ptheta": len(pats),
        "RZ_size": len(RZ),
        "dim_us": dim,
        "H2": h2,
        "d": list(d),
        "q": list(q0),
    }
    for key, value in expected.items():
        if got[key] != value:
            raise AssertionError(f"{name}: {key} expected {value}, got {got[key]}")
    return {**got, "expected": expected, "ok": True}


def main():
    cfg = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
    rows = [
        row(
            cfg,
            "4x4",
            [(x, y) for x in range(4) for y in range(4)],
            {"size": 16, "Ptheta": 35, "RZ_size": 4, "dim_us": 13, "H2": 17},
        ),
        row(
            cfg,
            "hex17",
            poly([(1, 0), (3, 0), (4, 2), (3, 4), (1, 4), (0, 2)]),
            {"size": 17, "Ptheta": 37, "RZ_size": 5, "dim_us": 13, "H2": 18},
        ),
    ]
    path = ART / "validation-examples.json"
    path.write_text(json.dumps(rows, indent=1), encoding="utf-8")
    for r in rows:
        print(
            f"{r['window']}: |S|={r['size']} P={r['Ptheta']} |RZ|={r['RZ_size']} "
            f"dim={r['dim_us']} H2={r['H2']} d={r['d']} q={r['q']}"
        )
    print("wrote", path)


if __name__ == "__main__":
    main()
