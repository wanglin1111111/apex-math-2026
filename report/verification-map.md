# Apex Math 候选论证验证地图

快照：2026-10-26T22:57:03.188249+00:00。数据源：math.apexin.net 公开 API。

> 23 条里没有一条是“给出具体反例/具体失效步骤”的重大漏洞条目；唯一 kind=challenge 的 #23 是部分 Lean 形式化。P2/P3 的“全篇 Lean”是作者声称，不是本页独立复核的结论。

## P1 · Seifert / Kakimizu

Contractibility of the complex of incompressible Seifert surfaces

重点：Theorem A（纽结）、B（交换复形）、C（截断）、D（链接） · [论文 PDF](https://math.apexin.net/papers/seifert-surfaces.pdf)

| # | 状态 | 作品 | 作者/票 | 本页备注 |
|---|---|---|---|---|
| [#10](https://math.apexin.net/api/v1/challenges/10) | 作者声称完整 | A complete Lean 4 formalization of Theorem B: every exchange complex is contractible | user_180f5e / 2 | Theorem B 完整 Lean；A/C/D 明确标注仅条件验证 |
| [#14](https://math.apexin.net/api/v1/challenges/14) | 独立审计/复算 | Key verification of the incompressible exchange lemma (Theorem 5.1): structured line-by-line audit with corrections | user_180f5e / 0 | Theorem 5.1 的 87 步逐行审计；作者声明是纸笔审计，不是形式化 |
| [#15](https://math.apexin.net/api/v1/challenges/15) | 补充/推广 | Fixed-point contractibility for exchange complexes and incompressible Seifert surfaces | user_180f5e / 0 | 不动点/等变版本的补充 |
| [#16](https://math.apexin.net/api/v1/challenges/16) | 缺口修补 | Repairing the compactness input of Kakimizu-complex contractibility: boundary compactness for exact minimizers | user_180f5e / 0 | 指出并修补紧致性输入缺口；作者声明不是反例 |
| [#17](https://math.apexin.net/api/v1/challenges/17) | 补充/推广 | Open question (F) of the Seifert-surface paper answered: a prime counterexample, and finiteness for atoroidal knots | user_180f5e / 0 | 开问题 (F) 的反例 + 环面纽结有限性 |
| [#19](https://math.apexin.net/api/v1/challenges/19) | 独立审计/复算 | Independent verification of the geometric half of Theorem A (§§3–5, Appendices A–B): six local points repaired | user_50c6c8 / 0 | Theorem A 几何部分 + §6.2 的独立审计，列出六处修补 G1–G6 |
| [#20](https://math.apexin.net/api/v1/challenges/20) | 独立审计/复算 | Independent verification of Fin compactness with sliding longitude boundary | user_d62a77 / 2 | Fin 紧致性与滑动经线边界的独立验证 |
| [#21](https://math.apexin.net/api/v1/challenges/21) | 部分/条件 | Partial link extensions: Hopf fibre links, annular satellites, and connected sums | user_180f5e / 0 | 只做 Hopf 纤维链等部分链接扩展；不主张全链接 |
| [#23](https://math.apexin.net/api/v1/challenges/23) | 部分/条件 | A partial Lean 4 formalization of the full paper | user_d3d67e / 0 | 部分 Lean 形式化，归在 challenge 类；不是具体缺口指控 |

## P2 · Curve complex, genus 2

The complex of curves pairwise intersecting at most once is contractible in genus two

重点：C₁(S₂) 可缩；Souto 问题的 genus 2 情形 · [论文 PDF](https://math.apexin.net/papers/curve-complex-genus-two.pdf)

| # | 状态 | 作品 | 作者/票 | 本页备注 |
|---|---|---|---|---|
| [#1](https://math.apexin.net/api/v1/challenges/1) | 独立审计/复算 | Exhaustive finite validation of the six-point Budget lemmas in the genus-two curve-complex paper | user_180f5e / 0 | 六点 Budget 引理的穷举验证 |
| [#2](https://math.apexin.net/api/v1/challenges/2) | 独立审计/复算 | Validation of the original augmented spectral-sequence step in the genus-two paper | user_180f5e / 0 | 增广谱序列步骤的验证 |
| [#3](https://math.apexin.net/api/v1/challenges/3) | 补充/推广 | A stratumwise strong deformation retraction for the genus-two curve complex | user_180f5e / 2 | 分层强形变收缩，补强定理 1.1 |
| [#11](https://math.apexin.net/api/v1/challenges/11) | 部分/条件 | Conditional Lean verification of genus-two 1-curve complex contractibility: arc retraction and arc–curve correspondence | user_180f5e / 0 | 条件 Lean：弧收缩与弧–曲线对应 |
| [#12](https://math.apexin.net/api/v1/challenges/12) | 部分/条件 | Conditional Lean verification of genus-two 1-curve complex contractibility from reviewed classical inputs | user_180f5e / 0 | 条件 Lean：来自已审经典输入 |
| [#13](https://math.apexin.net/api/v1/challenges/13) | 作者声称完整 | A complete Lean 4 formalization of the full paper | user_d3d67e / 3 | 全篇 Lean；作者声称无 sorry/admit，公理审计为标准三条 |
| [#22](https://math.apexin.net/api/v1/challenges/22) | 补充/推广 | Higher Connectivity, Fixed Points, and an Equivariance Obstruction for Curve Complexes | user_180f5e / 1 | 高阶连通、不动点与等变障碍 |

## P3 · Convex Nivat

The convex Nivat conjecture

重点：Theorem A（星形配置）、Theorem B（凸 Nivat 归约） · [论文 PDF](https://math.apexin.net/papers/convex-nivat.pdf)

| # | 状态 | 作品 | 作者/票 | 本页备注 |
|---|---|---|---|---|
| [#4](https://math.apexin.net/api/v1/challenges/4) | 独立审计/复算 | Verification of Theorem A for Star Configurations in the Convex Nivat Paper | user_180f5e / 0 | Theorem A §§0–7 验证；附录 C 解释性错误不影响主线 |
| [#5](https://math.apexin.net/api/v1/challenges/5) | 独立审计/复算 | Validation of the reduction to star configurations in the convex Nivat paper | user_180f5e / 2 | §8 + 附录 D 归约验证；Theorem A 作为输入 |
| [#6](https://math.apexin.net/api/v1/challenges/6) | 作者声称完整 | Theorem B（定理 8.18）的 Lean 形式化验证：完整证明依赖、题意对应与公理审计 | user_be06ff / 1 | Theorem B（8.18）完整 Lean；不是全篇 |
| [#7](https://math.apexin.net/api/v1/challenges/7) | 补充/推广 | Complementary complexity bounds for Case B star configurations: convex sections and all quadratic positions | user_180f5e / 1 | Case B 星形配置的互补复杂度界 |
| [#8](https://math.apexin.net/api/v1/challenges/8) | 补充/推广 | A scalar bridge replacing the spectral and background modules of the convex Nivat star proof | user_180f5e / 1 | scalar bridge 替代谱/背景模块；作者声明不转移附录 C 证书 |
| [#9](https://math.apexin.net/api/v1/challenges/9) | 独立审计/复算 | 凸形 Nivat 论文引理 5.2 的商代数核验与精确证书 | user_b29767 / 0 | Lemma 5.2 商代数核验 + 精确证书 |
| [#18](https://math.apexin.net/api/v1/challenges/18) | 作者声称完整 | A complete Lean 4 formalization of the full paper | user_d3d67e / 3 | 全篇 Lean；作者声称覆盖 49 个原论文结果；附录 C 原脚本未提供，未声称复跑 |

## 还缺什么

- **P1**：重大漏洞类没有真正的缺口/反例条目。 Theorem D 没有独立的无条件验证：#10 只做条件形式化，#19 只读了链接部分，#21 只覆盖 Hopf 子类。
- **P2**：重大漏洞类没有真正的缺口/反例条目。 论文自己说明方法不外推到 g ≥ 3；带 puncture/边界的情形也未处理。
- **P3**：重大漏洞类没有真正的缺口/反例条目。 附录 C 的 star.py/verify.py 未随 PDF/公开 Math-Paper 仓库提供；#18 明确说原脚本没有复现。
- **全局**：23 条里没有一条是“给出具体反例/具体失效步骤”的 challenge。 唯一 kind=challenge 的 #23 是部分 Lean 形式化，不是缺口指控。

## 本仓库的独立检查（P3 · Experiment 2 家族）

- 1000 组配置 × 8 窗口 = 8000 项精确检查；违例 0。
- 找到 1695 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对；抽查 60 组，60/60 通过。
- 复现论文代表行：4×4 窗口 Pθ=35、|RZ|=4、dim U_S=13、H2=17；hex17 窗口 Pθ=37、|RZ|=5、dim U_S=13、H2=18。
- 范围：只覆盖 Experiment 2 的 m=2、k=1、常数尾家族；不覆盖 m=3 的 Case-B/RZ，也不构成对 Theorem T 的证明。
