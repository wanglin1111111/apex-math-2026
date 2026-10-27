"""Completeness (padding-fixpoint) regression for `exact_patterns`.

Backs Lemma 3 in report/EXACTNESS.md: with padding = max|det(v_i,v_j)|, every
residue class of the image lattice is represented inside the enumeration box,
so doubling the padding cannot add a pattern.  This script asserts exactly
that fixpoint property on a fixed pseudo-random family (deterministic seed),
so "completeness" becomes a reproducible, regressable property rather than a
hand-waving claim.

Usage:
    python proof_check_exactness.py            # quick (default family)
    python proof_check_exactness.py --n 2000   # larger sweep
Exit 0  <=>  no configuration/width window gained a pattern from doubling.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from star import Experiment2Config, det  # noqa: E402

# a superset of the paper's Appendix C.2 direction list, on purpose:
# larger determinants stress the padding bound harder.
DIRS = [(1, 0), (0, 1), (1, 1), (1, -1), (1, 2), (1, -2), (2, 1), (2, -1),
        (1, 3), (1, -3), (3, 1), (1, 4), (4, 1), (2, 3), (3, 2), (5, 2)]


def rect(w: int, h: int):
    return [(x, y) for x in range(w) for y in range(h)]


WINS = {
    "4x4": rect(4, 4),
    "6x6": rect(6, 6),
    "8x5": rect(8, 5),
    "hex17": [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1), (0, 2),
              (1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3),
              (1, 4), (2, 4), (3, 4)],
}


def random_cfg(rng: random.Random, p: int):
    m = 2
    dirs = rng.sample(DIRS, m)
    consts = [rng.randrange(p) for _ in range(m)]
    wins, vals = [], []
    for i in range(m):
        L = rng.randint(1, 4)
        s = rng.randint(-3, 3)
        v = [rng.randrange(p) for _ in range(L)]
        if all(x == consts[i] for x in v):
            v[rng.randrange(L)] = (consts[i] + 1) % p
        wins.append([s, L])
        vals.append(v)
    return Experiment2Config(p, dirs, consts, wins, vals)


def max_det(cfg: Experiment2Config) -> int:
    return max(abs(det(cfg.directions[i], cfg.directions[j]))
               for i in range(cfg.m) for j in range(i + 1, cfg.m))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261027)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    checked = 0
    fails = 0
    for trial in range(args.n):
        p = rng.choice([2, 3, 5])
        cfg = random_cfg(rng, p)
        rho = max_det(cfg)
        for wname, S in WINS.items():
            base = cfg.exact_patterns(S)                    # padding = rho
            double = cfg.exact_patterns(S, padding=2 * rho)  # padding = 2 rho
            checked += 1
            if base != double:
                fails += 1
                print(f"FAIL trial={trial} {wname} p={p} dirs={cfg.directions} "
                      f"rho={rho} |base|={len(base)} |double|={len(double)} "
                      f"gained={len(double - base)}")

    print(f"completeness fixpoint: {checked - fails}/{checked} pairs unchanged "
          f"under padding double (n={args.n})")
    if fails == 0:
        print("PASS: padding = max|det| is sufficient (no new pattern from doubling)")
        return 0
    print("FAIL", fails)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
