"""Independent checker for the star-configuration part of the convex Nivat paper.

This module implements the Experiment 2 family from Appendix C.2:
theta = sum_i w_i(pi_i(z)), with k_i = 1 and constant tails.
No code from the paper or from existing submissions is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd
from typing import Iterable, Sequence

Vec = tuple[int, int]


def det(a: Vec, b: Vec) -> int:
    return a[0] * b[1] - a[1] * b[0]


def dot(a: Vec, b: Vec) -> int:
    return a[0] * b[0] + a[1] * b[1]


def primitive(v: Vec) -> bool:
    return gcd(abs(v[0]), abs(v[1])) == 1


def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1])


def scale(k: int, v: Vec) -> Vec:
    return (k * v[0], k * v[1])


def pi(v: Vec, z: Vec) -> int:
    """pi_v(z) = det(v, z)."""
    return det(v, z)


def find_basis(v: Vec) -> Vec:
    """Return u with det(v, u) = 1."""
    a, b = v
    # solve a*u_y - b*u_x = 1 with extended gcd
    g, x, y = extended_gcd(a, -b)
    if g != 1:
        raise ValueError(f"direction not primitive: {v}")
    # a*x + (-b)*y = 1 -> u = (y, x)
    return (y, x)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = extended_gcd(b, a % b)
    return (g, y, x - (a // b) * y)


def lattice_points_in_polygon(poly: Sequence[Vec]) -> set[Vec]:
    """All integer points inside or on a lattice polygon (convex hull)."""
    if not poly:
        return set()
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out: set[Vec] = set()
    for x in range(min(xs), max(xs) + 1):
        for y in range(min(ys), max(ys) + 1):
            if point_in_convex((x, y), poly):
                out.add((x, y))
    return out


def convex_hull(points: Iterable[Vec]) -> list[Vec]:
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o: Vec, a: Vec, b: Vec) -> int:
        return det(sub(a, o), sub(b, o))

    lower: list[Vec] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Vec] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def point_in_convex(p: Vec, poly: Sequence[Vec]) -> bool:
    """Convex polygon, counter-clockwise or clockwise, boundary included."""
    n = len(poly)
    if n == 0:
        return False
    if n == 1:
        return p == poly[0]
    if n == 2:
        a, b = poly
        return det(sub(b, a), sub(p, a)) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    sign = 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        c = det(sub(b, a), sub(p, a))
        if c != 0:
            s = 1 if c > 0 else -1
            if sign == 0:
                sign = s
            elif sign != s:
                return False
    return True


def solve_pi_pair(v1: Vec, v2: Vec, t1: int, t2: int) -> Vec | None:
    """Return z in Z^2 with pi(v1,z)=t1 and pi(v2,z)=t2, if it exists."""
    D = det(v1, v2)
    if D == 0:
        raise ValueError("parallel directions")
    # pi(v,z) = v_x*z_y - v_y*z_x
    # matrix [[-v1_y, v1_x], [-v2_y, v2_x]] * [z_x, z_y] = [t1, t2]
    a, b = -v1[1], v1[0]
    c, d = -v2[1], v2[0]
    # Cramer
    nx = t1 * d - b * t2
    ny = a * t2 - t1 * c
    if nx % D != 0 or ny % D != 0:
        return None
    return (nx // D, ny // D)


@dataclass
class Experiment2Config:
    p: int
    directions: list[Vec]
    constants: list[int]
    windows: list[tuple[int, int]]  # (start, length)
    values: list[list[int]]  # values[i][j] for pi_i = start+j

    def __post_init__(self) -> None:
        if len(self.directions) != len(self.constants) or len(self.directions) != len(self.windows) or len(self.directions) != len(self.values):
            raise ValueError("length mismatch")
        for v in self.directions:
            if not primitive(v):
                raise ValueError(f"direction not primitive: {v}")
        for i, (start, length) in enumerate(self.windows):
            if length < 1 or len(self.values[i]) != length:
                raise ValueError("window/value mismatch")

    @property
    def m(self) -> int:
        return len(self.directions)

    def w(self, i: int, t: int) -> int:
        start, length = self.windows[i]
        if start <= t < start + length:
            return self.values[i][t - start] % self.p
        return self.constants[i] % self.p

    def F(self, i: int, z: Vec) -> int:
        return self.w(i, pi(self.directions[i], z))

    def theta(self, z: Vec) -> int:
        return sum(self.F(i, z) for i in range(self.m)) % self.p

    def is_star(self) -> bool:
        # S1: period v_i (k_i=1) holds by construction of w(pi_i).
        # S2: F_i is not doubly periodic iff w_i is not constant.
        for i in range(self.m):
            vals = {self.w(i, t) for t in range(self.windows[i][0], self.windows[i][0] + self.windows[i][1])}
            vals.add(self.constants[i] % self.p)
            if len(vals) == 1:
                return False
        # S3: constant tails hold by construction.
        return True

    def pattern(self, u: Vec, S: Sequence[Vec]) -> tuple[int, ...]:
        return tuple(self.theta(add(u, s)) for s in S)

    def patterns(self, S: Sequence[Vec], radius: int = 40) -> set[tuple[int, ...]]:
        out: set[tuple[int, ...]] = set()
        for ux in range(-radius, radius + 1):
            for uy in range(-radius, radius + 1):
                out.add(self.pattern((ux, uy), S))
        return out

    def exact_patterns(self, S: Sequence[Vec], padding: int | None = None) -> set[tuple[int, ...]]:
        """Exact pattern set for the Experiment 2 family.

        The pattern depends only on t_i = pi_i(u).  It can change only when
        t_i + pi_i(s) crosses a window boundary, so every possible pattern is
        represented by an integer tuple in a bounded box around those
        breakpoints.  Each tuple is then tested for being in the image of
        u -> (pi_1(u), ..., pi_m(u)).

        A padding of one full period of the image lattice is included so that
        far-away representatives of every residue class are not missed.
        """
        if padding is None:
            max_det = 1
            for i in range(self.m):
                for j in range(i + 1, self.m):
                    max_det = max(max_det, abs(det(self.directions[i], self.directions[j])))
            padding = max_det
        ranges: list[range] = []
        for i in range(self.m):
            start, length = self.windows[i]
            bp: set[int] = set()
            for s in S:
                t = pi(self.directions[i], s)
                bp.add(start - t)
                bp.add(start + length - t)
            lo, hi = min(bp) - 1, max(bp) + 1
            ranges.append(range(lo - padding, hi + padding + 1))
        out: set[tuple[int, ...]] = set()
        for ts in product(*ranges):
            u = solve_pi_pair(self.directions[0], self.directions[1], ts[0], ts[1])
            if u is None:
                continue
            if any(pi(self.directions[i], u) != ts[i] for i in range(2, self.m)):
                continue
            pat = []
            for s in S:
                val = 0
                for i in range(self.m):
                    val += self.w(i, ts[i] + pi(self.directions[i], s))
                pat.append(val % self.p)
            out.add(tuple(pat))
        return out

    def support_t(self, i: int) -> set[int]:
        start, length = self.windows[i]
        c = self.constants[i] % self.p
        return {t for t in range(start, start + length) if self.w(i, t) != c}

    def case_b_m2(self) -> bool:
        """Observation C.1 for m=2: Case B iff supports are disjoint in Z^2."""
        if self.m != 2:
            raise ValueError("only for m=2")
        v1, v2 = self.directions
        s1, s2 = self.support_t(0), self.support_t(1)
        for t1 in s1:
            for t2 in s2:
                if solve_pi_pair(v1, v2, t1, t2) is not None:
                    return False
        return True

    def case_ab(self, radius: int = 30) -> tuple[str, tuple[int, int, int] | None]:
        """Compute D I_a on a box. Returns ('A', witness) or ('B', None)."""
        H = [v for v in self.directions]  # k_i=1, M=1
        for a in range(self.p):
            for ux in range(-radius, radius + 1):
                for uy in range(-radius, radius + 1):
                    z = (ux, uy)
                    total = 0
                    for mask in range(1 << self.m):
                        s = (0, 0)
                        bits = 0
                        for i in range(self.m):
                            if mask & (1 << i):
                                s = add(s, H[i])
                                bits += 1
                        sign = -1 if (self.m - bits) % 2 else 1
                        if self.theta(add(z, s)) == a:
                            total += sign
                    if total != 0:
                        return ("A", (a, ux, uy))
        return ("B", None)


def zonotope_vertices(directions: Sequence[Vec], d: Sequence[int]) -> list[Vec]:
    m = len(directions)
    pts = [(0, 0)]
    for i in range(m):
        pts = [add(p, scale(k, directions[i])) for p in pts for k in (0, d[i])]
    return convex_hull(pts)


def zonotope_lattice_points(directions: Sequence[Vec], d: Sequence[int]) -> set[Vec]:
    verts = zonotope_vertices(directions, d)
    return lattice_points_in_polygon(verts)


def rz_points(S: Sequence[Vec], directions: Sequence[Vec], d: Sequence[int]) -> list[Vec]:
    poly = convex_hull(S)
    verts = zonotope_vertices(directions, d)
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    out: list[Vec] = []
    for rx in range(min(xs) - 8, max(xs) + 9):
        for ry in range(min(ys) - 8, max(ys) + 9):
            r = (rx, ry)
            if all(point_in_convex(add(r, v), poly) for v in verts):
                out.append(r)
    return out


def rank_mod_q(rows: Sequence[Sequence[int]], q: int) -> int:
    """Rank of a matrix over F_q, q prime."""
    if not rows:
        return 0
    mat = [list(r) for r in rows]
    n_rows = len(mat)
    n_cols = len(mat[0])
    rank = 0
    for col in range(n_cols):
        pivot = None
        for r in range(rank, n_rows):
            if mat[r][col] % q:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, q - 2, q)
        mat[rank] = [(x * inv) % q for x in mat[rank]]
        for r in range(n_rows):
            if r != rank and mat[r][col] % q:
                factor = mat[r][col] % q
                mat[r] = [(a - factor * b) % q for a, b in zip(mat[r], mat[rank])]
        rank += 1
        if rank == n_rows:
            break
    return rank


def dim_us(patterns: Sequence[tuple[int, ...]], S: Sequence[Vec], w: dict[int, int], q: int) -> int:
    rows = [[1] + [w[g] for g in pat] for pat in patterns]
    return rank_mod_q(rows, q)


def find_d_q(config: Experiment2Config, S: Sequence[Vec], radius: int = 20) -> tuple[Vec, Vec] | None:
    """Find d != 0 with J(d,.) != 0 and q with q, q+d in Z_lattice."""
    Zpts = zonotope_lattice_points(config.directions, [1] * config.m)
    Zset = set(Zpts)
    # eta = w(theta); use w(a)=a+1, injective.
    wmap = {a: a + 1 for a in range(config.p)}

    def eta(z: Vec) -> int:
        return wmap[config.theta(z)]

    def D_eta_product(z: Vec, d: Vec) -> int:
        total = 0
        for mask in range(1 << config.m):
            s = (0, 0)
            bits = 0
            for i in range(config.m):
                if mask & (1 << i):
                    s = add(s, config.directions[i])
                    bits += 1
            sign = -1 if (config.m - bits) % 2 else 1
            total += sign * eta(add(z, s)) * eta(add(add(z, s), d))
        return total

    for q0 in Zpts:
        for q1 in Zpts:
            d = sub(q1, q0)
            if d == (0, 0):
                continue
            for ux in range(-radius, radius + 1):
                for uy in range(-radius, radius + 1):
                    if D_eta_product((ux, uy), d) != 0:
                        return (d, q0)
    return None


def h2_rank(
    config: Experiment2Config,
    S: Sequence[Vec],
    patterns: Sequence[tuple[int, ...]],
    w: dict[int, int],
    RZ: Sequence[Vec],
    d: Vec,
    q0: Vec,
    q: int,
) -> int:
    rows: list[list[int]] = []
    for pat in patterns:
        base = [1] + [w[g] for g in pat]
        extra = [w[pat[S.index(add(r, q0))]] * w[pat[S.index(add(add(r, q0), d))]] for r in RZ]
        rows.append(base + extra)
    return rank_mod_q(rows, q)
