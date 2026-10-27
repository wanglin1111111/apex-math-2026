"""Unit tests for the independent Experiment-2 checker."""

import unittest

from star import (
    Experiment2Config,
    convex_hull,
    det,
    dim_us,
    find_d_q,
    h2_rank,
    lattice_points_in_polygon,
    rz_points,
    zonotope_lattice_points,
)


def rect(w, h):
    return [(x, y) for x in range(w) for y in range(h)]


def poly(verts):
    return sorted(lattice_points_in_polygon(convex_hull(verts)))


WINDOWS = {
    "3x4": rect(3, 4),
    "4x4": rect(4, 4),
    "hex17": poly([(1, 0), (3, 0), (4, 2), (3, 4), (1, 4), (0, 2)]),
}


class StarTests(unittest.TestCase):
    def test_hand_case_a(self):
        cfg = Experiment2Config(3, [(1, 0), (0, 1)], [0, 0], [(0, 1), (0, 1)], [[1], [1]])
        self.assertTrue(cfg.is_star())
        self.assertFalse(cfg.case_b_m2())
        self.assertEqual(cfg.case_ab(radius=10)[0], "A")
        S = [(0, 0), (1, 0)]
        self.assertEqual(len(cfg.exact_patterns(S)), 6)
        self.assertGreaterEqual(len(cfg.exact_patterns(S)), len(S) + 1)

    def test_paper_row_4x4(self):
        cfg = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
        S = WINDOWS["4x4"]
        pats = sorted(cfg.exact_patterns(S))
        RZ = rz_points(S, cfg.directions, [1, 1])
        w = {a: a + 1 for a in range(cfg.p)}
        q = 2**31 - 1
        self.assertEqual(len(pats), 35)
        self.assertEqual(len(RZ), 4)
        self.assertEqual(dim_us(pats, S, w, q), 13)
        dq = find_d_q(cfg, S, radius=10)
        self.assertIsNotNone(dq)
        d, q0 = dq
        self.assertEqual(h2_rank(cfg, S, pats, w, RZ, d, q0, q), 17)

    def test_paper_row_hex17(self):
        cfg = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
        S = WINDOWS["hex17"]
        pats = sorted(cfg.exact_patterns(S))
        RZ = rz_points(S, cfg.directions, [1, 1])
        w = {a: a + 1 for a in range(cfg.p)}
        q = 2**31 - 1
        self.assertEqual(len(pats), 37)
        self.assertEqual(len(RZ), 5)
        self.assertEqual(dim_us(pats, S, w, q), 13)
        d, q0 = find_d_q(cfg, S, radius=10)
        self.assertEqual(h2_rank(cfg, S, pats, w, RZ, d, q0, q), 18)

    def test_exact_matches_sampling(self):
        cfg = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
        for S in WINDOWS.values():
            self.assertEqual(cfg.exact_patterns(S), cfg.patterns(S, radius=60))

    def test_constant_config_rejected(self):
        cfg = Experiment2Config(3, [(1, 0), (0, 1)], [0, 0], [(0, 2), (0, 2)], [[0, 0], [0, 0]])
        self.assertFalse(cfg.is_star())
        S = WINDOWS["3x4"]
        self.assertLess(len(cfg.exact_patterns(S)), len(S) + 1)

    def test_case_criterion_agrees_with_D(self):
        configs = [
            Experiment2Config(3, [(1, 0), (0, 1)], [0, 0], [(0, 1), (0, 1)], [[1], [1]]),
            Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]]),
            Experiment2Config(2, [(1, -3), (3, 1)], [1, 0], [(-2, 2), (-3, 1)], [[1, 0], [1]]),
        ]
        for cfg in configs:
            expected = "B" if cfg.case_b_m2() else "A"
            self.assertEqual(cfg.case_ab(radius=30)[0], expected)

    def test_rank_negative_control(self):
        cfg = Experiment2Config(3, [(1, 0), (1, 2)], [0, 0], [(0, 1), (1, 1)], [[1], [1]])
        S = WINDOWS["hex17"]
        pats = sorted(cfg.exact_patterns(S))
        RZ = rz_points(S, cfg.directions, [1, 1])
        q = 2**31 - 1
        self.assertEqual(dim_us(pats, S, {a: a + 1 for a in range(cfg.p)}, q), 13)
        bad = {a: 0 for a in range(cfg.p)}
        self.assertEqual(dim_us(pats, S, bad, q), 1)
        self.assertNotEqual(dim_us(pats, S, bad, q), 13)

    def test_padding_regression(self):
        cfg = Experiment2Config(2, [(1, -3), (3, 1)], [1, 0], [(-2, 2), (-3, 1)], [[1, 0], [1]])
        S = WINDOWS["3x4"]
        small = cfg.exact_patterns(S, padding=1)
        full = cfg.exact_patterns(S, padding=10)
        self.assertLess(len(small), len(full))
        self.assertEqual(len(full), 15)
        two_zeros = (1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1)
        self.assertIn(two_zeros, full)
        self.assertNotIn(two_zeros, small)


if __name__ == "__main__":
    unittest.main()
