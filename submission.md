# Independent exact verification of the Experiment 2 family for the convex Nivat paper

**Paper:** *The Convex Nivat Conjecture: A Complexity Lower Bound for Star Configurations, and a Reduction from Low Convex Complexity to Star Configurations* (Apex Intelligence, 12 September 2026).

**Paper PDF SHA-256:** `7fd67831155f4226c010fd6af32de558b76643771e6be12dea4eebafa21745a8`.

**Contribution category:** Key verification (verification).

**Repository:** REPO_URL

**Verification map:** REPO_URL/report/verification-map.html

**Artifact manifest:** REPO_URL/report/SHA256SUMS.txt

## 摘要（中文）

本投稿对凸 Nivat 论文附录 C.2 的 Experiment 2 家族做独立、精确的有限验证：从零实现星形配置生成器、精确 Pθ(S) 枚举、Case A/B 判定、zonotope/RZ(S)、dim U_S 与 H2(S) 秩检查。共检查 1,000 组配置 × 8 个附录 C.2 窗口 = 8,000 项，未发现 Pθ(S) < |S|+1 的反例；找到 1,695 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对，抽查 60 组秩检查全部满足 dim U_S = |S|+1−|RZ(S)| 与 H2(S) = |S|+1。另外复现了论文 Appendix C.2 两条代表行的 Pθ、|RZ|、dim U_S 与 H2（4×4 与 hex17；d 取另一组合法见证）。这是有限验证，不是对 Theorem T 的证明；范围仅限 m=2、k=1、常数尾的 Experiment 2 家族。

## Summary (English)

This submission is an independent, exact finite verification of the Experiment 2 family in Appendix C.2 of the convex Nivat paper. The checker is implemented from scratch: a star-configuration generator, exact pattern counting Pθ(S), Case A/B classification, the zonotope and RZ(S), and the dim U_S / H2(S) rank checks.

- **8,000 exact window checks** (1,000 configurations × 8 Appendix C.2 windows).
- **No violation** of Pθ(S) ≥ |S|+1.
- **1,695** configuration-window pairs with Case B and RZ(S) ≠ ∅.
- **60 sampled rank checks**, all **60/60** satisfy dim U_S = |S|+1−|RZ(S)| and H2(S) = |S|+1.
- Two representative rows of Appendix C.2 are reproduced: the reported Pθ, |RZ|, dim U_S and H2 values match (with another valid witness d).

This is a finite verification, not a proof of Theorem T. The scope is the m=2, k=1, constant-tail Experiment 2 family.

## What is and is not claimed

**Claimed.** For every generated configuration in the stated family and every one of the eight Appendix C.2 windows, the exact pattern count satisfies the theorem's inequality. The Case-B/RZ rank identities hold on the sampled instances. The two reported table rows are reproduced.

**Not claimed.** This is not a proof of Theorem T, not a verification of the paper's Experiment 1 family, not a verification of general star configurations, and not an exact reproduction of the paper's original 84 + 157 random runs. The paper's `star.py`, `verify.py`, `verify2.py` and their saved outputs were not supplied with the PDF or the public Math-Paper repository; the random seeds alone do not determine the runs without the original RNG and generation order. This work therefore does not claim to reproduce those exact runs. It also makes no m=3 Case-B/RZ claim; the paper's generator produced no such instance with RZ(S) ≠ ∅.

## Method

### Configuration family

Each component is `F_i(z) = w_i(π_i(z))`, where `π_i(z) = det(v_i,z)`, `w_i: Z → F_p` is constant `c_i` outside a finite interval and arbitrary inside it, and `L_i = R_i = c_i`. Thus `k_i = 1`; the constant tails are doubly periodic and every configuration is a star configuration in the sense of §0.1, provided at least one value inside each window differs from `c_i` (S2). The 11 directions are those listed in Appendix C.2. The generator chooses `p ∈ {2,3,5}`, two distinct non-parallel directions, constants and windows; a targeted branch also constructs Case-B instances by choosing supports whose two line families do not meet in Z².

### Exact pattern counting

The pattern on S depends only on `t_i = π_i(u)`. It can change only when `t_i + π_i(s)` crosses a window boundary for some `s ∈ S`. The checker enumerates every integer tuple `(t_1,…,t_m)` in a bounded box around those breakpoints, tests whether it is in the image of `u ↦ (π_1(u),…,π_m(u))` by solving the two linear equations `π_1(u)=t_1`, `π_2(u)=t_2` and checking the remaining coordinates, and evaluates the pattern at a realizing `u`.

A padding of one full period of the image lattice is included on each side. This is necessary: far-away representatives of a residue class can realize patterns that are not represented by the single nearest far point. The first version of the checker used one far representative only and undercounted three patterns in one configuration; the final version fixes this (see below). The padding is set from the largest determinant of a pair of directions.

### Case A/B, zonotope, and ranks

For m=2, Case B is decided exactly by Observation C.1: it holds iff the supports of the deviation fields `δ_i = F_i − c_i` are disjoint in Z². The checker compares this criterion with the direct `D I_a` computation on sample configurations; they agree.

For a Case-B instance, `Λ_i = {1}`, `d_i = 1`, and `Z = [0,v_1] + [0,v_2]`. The checker computes `RZ(S) = {r ∈ Z² : r+Z ⊆ Conv(S)}` by testing the zonotope vertices, the sampled rank `dim U_S` of the matrix `[1, w(γ(s))]` over the pattern set, and the extended rank `H2(S)` using a witness `d` and `q` from §5–§7. Ranks are computed over `F_q` with `q = 2^31 − 1` by modular Gaussian elimination. The encoding is `w(a)=a+1`; injectivity and the spectrum condition are checked on the reported instances.

## Results

The search used 1,000 configurations (deterministic seeds derived from `20261027`) and the eight Appendix C.2 windows: 3×4, 4×4, 5×3, 4×3 rectangles, the 15-point triangle, the 17-point hexagon, the 13-point rhombus, and the 12-point parallelogram.

| item | value |
|---|---:|
| configurations | 1,000 |
| window checks | 8,000 |
| violations of Pθ(S) ≥ \|S\|+1 | **0** |
| Case-A window rows | 2,344 |
| Case-B window rows | 5,656 |
| Case-B and RZ(S) ≠ ∅ pairs | 1,695 |
| sampled rank checks | 60 |
| rank checks passing | **60/60** |

The 60 rank-check rows are in `artifacts/caseb-rank-results.csv`; every row has `rank_ok = True`, `dim_us = expected_dim`, and `H2 = expected_H2`. The full 8,000 rows are in `artifacts/search-results.csv`; all have `holds = True`.

## Reproduced Appendix C.2 rows

Using `p=3`, directions `(1,2)` and `(1,0)`, constants `(0,0)`, and transition supports at `t_1=0`, `t_2=1`, the checker gives:

| window | \|S\| | Pθ(S) | \|RZ(S)\| | dim U_S | H2(S) |
|---|---:|---:|---:|---:|---:|
| 4×4 | 16 | 35 | 4 | 13 | 17 |
| hex17 | 17 | 37 | 5 | 13 | 18 |

These match the first two representative rows of Appendix C.2 in Pθ, |RZ|, dim U_S and H2. The paper's rows list `d=(−1,−1)`; this implementation finds `d=(0,−1)` and `q=(1,2)`, another valid witness pair. The rank identities are identical.

## Validation, negative controls, and a disclosed bug

The unit suite has 8 tests; all pass. The deliberately broken checker (padding=1) fails the regression test, which is the red side of the red→green control:

```text
$ python bad_padding_test.py
test_padding_regression ... FAIL
AssertionError: 12 not less than 12
FAILED (failures=1)
exit=1
```

After restoring the checker, the same suite passes:

```text
$ cd code && python -m unittest discover -v
Ran 8 tests in 2.593s
OK
```

The negative controls show the checker rejects an invalid constant configuration and catches a corrupted encoding:

```text
$ python negative_controls.py
NEGATIVE CONTROL 1: constant configuration
is_star = False
Ptheta = 1 bound = 13
RED: invalid configuration rejected; if bypassed it would be a violation
POSITIVE CONTROL: valid configuration
Ptheta = 35 bound = 17
GREEN: theorem inequality holds on this instance
NEGATIVE CONTROL 2: corrupted encoding
dim_us(good) = 13
dim_us(bad)  = 1
RED: rank checker detects a corrupted encoding
```

**Disclosed bug.** The first version of the exact enumeration used only one far representative per coordinate and undercounted three patterns in one configuration (p=2, directions `(1,−3)`, `(3,1)`, supports `t_1=−1`, `t_2=−3`). This produced five false "violations" in the first 1,000-configuration run. A brute-force sample at radius 60 found the missing patterns; after adding the padding, exact enumeration and sampling agree on 80 equality cross-checks (10 configurations × 8 windows; radius 80), and the exact set was contained in the radius-80 sample on a further 240 checks (30 configurations × 8 windows). The fix is committed; the false positives are not part of the final result.

## Limitations

- Only the m=2, k=1, constant-tail Experiment 2 family is covered.
- The eight windows are the Appendix C.2 windows; the search is finite.
- The paper's original 84 + 157 random runs are not reproduced exactly; scripts and outputs were not supplied.
- The 60 rank checks are a sample of the 1,695 Case-B/RZ pairs, not exhaustive.
- The 1,000-configuration set includes a targeted Case-B branch; the 1,695 pairs are a search yield, not an estimate of the paper's Case-B frequency.
- No m=3 Case-B/RZ claim is made.
- No counterexample was found; a finite absence of counterexamples is not a proof of Theorem T.

## AI disclosure

This work was prepared with AI assistance. The submitter has **not line-by-line verified** every line of the code or every derivation. 中文：本工作由 AI 辅助完成，投稿人**未逐行人工复核**全部代码或推导。The finite checks, negative controls and reproduced rows are reproducible from the commands in `report/report.md`. This is not a human expert endorsement, and it does not claim to certify the full paper.

## Reproducibility

```sh
python code/run_search.py              # 1,000 configs × 8 windows; writes artifacts/
python code/validation_examples.py     # two Appendix C.2 rows; writes artifacts/validation-examples.json
cd code && python -m unittest discover -v
cd .. && python code/negative_controls.py
python code/build_map.py               # reader-facing verification map
python code/check_submission.py        # length and traceability checks
```

Environment: Python 3.11.9; standard library only (no third-party dependencies); 22 CPUs; no Lean, no pytest (unittest only).

## References

- Apex Intelligence, *The Convex Nivat Conjecture: A Complexity Lower Bound for Star Configurations, and a Reduction from Low Convex Complexity to Star Configurations*, 12 September 2026. `https://math.apexin.net/papers/convex-nivat.pdf`.
- Apex Math candidate-proof bounty announcement: `https://math.apexin.net/announcement`.
- Appendix C.2 of the paper (Experiment 2 family and the two representative rows).
