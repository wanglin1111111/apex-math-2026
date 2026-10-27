"""Negative controls: the checker must catch invalid configurations and bad encodings."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from star import (  # noqa: E402
    Experiment2Config,
    dim_us,
    rz_points,
)


def rect(w, h):
    return [(x, y) for x in range(w) for y in range(h)]


def main():
    S = rect(3, 4)
    bound = len(S) + 1

    constant = Experiment2Config(3, [(1, 0), (0, 1)], [0, 0], [(0, 2), (0, 2)], [[0, 0], [0, 0]])
    pats = constant.exact_patterns(S)
    print("NEGATIVE CONTROL 1: constant configuration")
    print("is_star =", constant.is_star())
    print("Ptheta =", len(pats), "bound =", bound)
    assert not constant.is_star()
    assert len(pats) < bound
    print("RED: invalid configuration rejected; if bypassed it would be a violation")

    valid = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
    S_valid = rect(4, 4)
    pats = sorted(valid.exact_patterns(S_valid))
    print("POSITIVE CONTROL: valid configuration")
    print("Ptheta =", len(pats), "bound =", len(S_valid) + 1)
    assert len(pats) >= len(S_valid) + 1
    print("GREEN: theorem inequality holds on this instance")

    good = {a: a + 1 for a in range(valid.p)}
    bad = {a: 0 for a in range(valid.p)}
    q = 2**31 - 1
    print("NEGATIVE CONTROL 2: corrupted encoding")
    print("dim_us(good) =", dim_us(pats, S_valid, good, q))
    print("dim_us(bad)  =", dim_us(pats, S_valid, bad, q))
    assert dim_us(pats, S_valid, bad, q) != dim_us(pats, S_valid, good, q)
    print("RED: rank checker detects a corrupted encoding")


if __name__ == "__main__":
    main()
