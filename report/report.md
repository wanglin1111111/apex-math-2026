# Independent exact verification of the Experiment 2 family

**Paper:** *The Convex Nivat Conjecture: A Complexity Lower Bound for Star Configurations, and a Reduction from Low Convex Complexity to Star Configurations* (Apex Intelligence, 12 September 2026).

**Paper PDF SHA-256:** `7fd67831155f4226c010fd6af32de558b76643771e6be12dea4eebafa21745a8` (verified 2026-10-27).

**Scope:** this is a finite, exact verification of the Experiment 2 family from Appendix C.2 (m=2, k=1, constant tails), not a proof of Theorem T. It is an independent reimplementation; no code from the paper or from any submission was used.

## 1. What was checked

For each generated configuration and each of the eight Appendix C.2 windows, the checker computes the exact pattern count Pθ(S) and compares it with |S|+1. It also classifies Case A/B, computes the zonotope Z, RZ(S), dim U_S and H2(S), and checks the rank identities for Case-B instances with RZ(S)≠∅.

- 1,000 configurations × 8 windows = **8,000 exact window checks**.
- **0 violations** of Pθ(S) ≥ |S|+1.
- **1,695** configuration-window pairs with Case B and RZ(S)≠∅.
- **60** sampled Case-B rank checks; **60/60** satisfy dim U_S = |S|+1−|RZ(S)| and H2(S) = |S|+1.
- Two representative rows of Appendix C.2 are reproduced: the reported Pθ, |RZ|, dim U_S and H2 values match (see §3).

## 2. Method

### 2.1 Configuration family

Each component is `F_i(z) = w_i(π_i(z))`, where `π_i(z) = det(v_i,z)`, `w_i: Z → F_p` is constant `c_i` outside a finite interval and arbitrary inside it, and the tails are `L_i = R_i = c_i`. Thus `k_i = 1`; every configuration is a star configuration in the sense of §0.1, provided at least one value inside each window differs from `c_i` (S2). The 11 directions are those listed in Appendix C.2.

### 2.2 Exact pattern enumeration

The pattern on S depends only on `t_i = π_i(u)`. It can change only when `t_i + π_i(s)` crosses a window boundary for some `s ∈ S`. The checker enumerates every integer tuple `(t_1,…,t_m)` in a bounded box around those breakpoints, tests whether it is in the image of `u ↦ (π_1(u),…,π_m(u))`, and evaluates the pattern at a realizing `u`.

A padding of one full period of the image lattice is included on each side, so far-away representatives of every residue class are not missed. This padding is essential: the first version used one far representative only and undercounted three patterns in one configuration (see §4).

### 2.3 Case A/B and ranks

For m=2, Case B is decided exactly by Observation C.1: it holds iff the supports of the deviation fields `δ_i = F_i − c_i` are disjoint in Z². The checker compares this criterion with the direct `D I_a` computation on sample configurations; they agree.

For a Case-B instance, `Λ_i = {1}`, `d_i = 1`, and `Z = [0,v_1] + [0,v_2]`. The checker computes `RZ(S)`, the sampled rank `dim U_S` of the matrix `[1, w(γ(s))]`, and the extended rank `H2(S)` using a witness `d` and `q` from §5–§7. Ranks are computed over `F_q` with `q = 2^31 − 1`.

## 3. Reproduced Appendix C.2 rows

Using `p=3`, directions `(1,2)` and `(1,0)`, constants `(0,0)`, and transition supports at `t_1=0`, `t_2=1`, the checker gives:

| window | \|S\| | Pθ(S) | \|RZ(S)\| | dim U_S | H2(S) |
|---|---:|---:|---:|---:|---:|
| 4×4 | 16 | 35 | 4 | 13 | 17 |
| hex17 | 17 | 37 | 5 | 13 | 18 |

These match the first two representative rows of Appendix C.2. The paper's rows list `d=(−1,−1)`; this implementation finds `d=(0,−1)` and `q=(1,2)`, which is another valid witness pair. The rank identities are identical.

## 4. Validation and one fixed bug

The unit suite has 8 tests and all pass:

```text
$ cd code && python -m unittest discover -v
test_case_criterion_agrees_with_D ... ok
test_constant_config_rejected ... ok
test_exact_matches_sampling ... ok
test_hand_case_a ... ok
test_padding_regression ... ok
test_paper_row_4x4 ... ok
test_paper_row_hex17 ... ok
test_rank_negative_control ... ok
Ran 8 tests in 2.593s
OK
```

The deliberately broken checker (padding=1) fails the regression test, which is the red side of the red→green control:

```text
$ python bad_padding_test.py
test_padding_regression ... FAIL
AssertionError: 12 not less than 12
FAILED (failures=1)
exit=1
```

After restoring the checker, the same suite passes (green, above). The bug was found during the 1,000-configuration run: five initial "violations" all came from one configuration whose exact enumeration missed three patterns with two zeros. A brute-force sample at radius 60 found the missing patterns. After adding the padding, exact enumeration and sampling agree on 80 equality cross-checks (10 configurations × 8 windows; radius 80), and the exact set was contained in the radius-80 sample on a further 240 checks (30 configurations × 8 windows). Both are reproduced by `code/cross_check.py` (evidence: `artifacts/cross-check.json`, 320/320 checks, 0 failures). This is disclosed because the first version would have produced a false counterexample claim.

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

## 5. Limitations

- Only the Experiment 2 family (m=2, k=1, constant tails) is covered. The paper's Experiment 1 family and general star configurations are not covered.
- The eight windows are the Appendix C.2 windows. The search is a finite exact check, not a proof of Theorem T.
- The paper's original 84 + 157 random configurations are not reproduced exactly: the scripts, RNG and saved outputs were not supplied with the PDF or the public Math-Paper repository. This work does not claim to reproduce those exact runs.
- The paper's generator produced no m=3 Case-B instance with RZ(S)≠∅; this work therefore makes no m=3 Case-B/RZ claim.
- The rank checks are sampled (60 of 1,695 Case-B/RZ pairs), not exhaustive.
- The 1,000-configuration set includes a targeted Case-B branch; the 1,695 pairs are a search yield, not an estimate of the paper's Case-B frequency.
- The search found no counterexample. A finite absence of counterexamples is not a proof.

## 6. Reproduce

```sh
cd apex-math-2026
python code/fetch_snapshot.py          # optional: refresh the public leaderboard snapshot
python code/run_search.py              # 1,000 configs × 8 windows; writes artifacts/
python code/validation_examples.py     # two Appendix C.2 rows; writes artifacts/validation-examples.json
cd code && python -m unittest discover -v
cd .. && python code/negative_controls.py
python code/build_map.py               # reader-facing map
python code/check_submission.py --allow-placeholder  # local pre-push; drop the flag after REPO_URL is replaced
```

Environment: Python 3.11.9; standard library only (no third-party dependencies); 22 CPUs; no Lean, no pytest (unittest only).

## 7. Traceability

The summary numbers in this report come from `artifacts/search-summary.json`. The two representative rows come from `artifacts/validation-examples.json`. The full per-window rows are in `artifacts/search-results.csv`, the Case-B rank rows in `artifacts/caseb-rank-results.csv`, and the inputs in `artifacts/configs.json`. SHA-256 values for every delivered artifact are in `report/SHA256SUMS.txt`.

## 8. AI disclosure

This work was prepared with AI assistance. The submitter has not line-by-line verified every line of the code or every derivation. The finite checks, negative controls and reproduced rows are reproducible from the commands above. This is not a human expert endorsement, and it does not claim to certify the full paper.
