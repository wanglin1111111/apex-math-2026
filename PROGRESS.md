# PROGRESS

## 2026-10-27 · 任务 0
- 目标：Paper 3（凸 Nivat）附录 C 独立复现 + 三篇论文×23 条作品的验证地图；同一投稿冲关键验证奖与社区选择奖。
- 顺序：任务 0 事实核对 → 任务 1 检查器 → 任务 2 搜索/复现 → 任务 3 地图 → 任务 4 投稿包 → 任务 5 人类提交闸门。
- 最大风险：附录 C 的 star.py/verify.py 未提供，Pθ(S) 精确计数与 Λi/zonotope/rank 需从零实现。
- 已核对：PDF SHA-256 `7fd67831155f4226c010fd6af32de558b76643771e6be12dea4eebafa21745a8` 一致；Python 3.11.9；仅标准库（无第三方依赖）；22 核；无 Lean/pytest。
- 快照：`artifacts/site-snapshot.json`（3 篇论文、23 条作品，2026-10-27 拉取）。

## 任务 1 · 检查器
- 实现 `code/star.py`：Experiment 2 生成器、精确 Pθ(S) 枚举、Case A/B、zonotope/RZ(S)、dim U_S 与 H2(S) 秩检查。
- `python -m unittest discover -v`：8 项全过（红→绿证据见 `report/report.md` §4）。
- 发现并修复 `exact_patterns` 的 padding 漏计：首版在 cid 489 上漏掉 3 个双零模式，产生 5 条假违例；修复后 80 项等值复核 + 240 项子集复核无差异。
- 负例：常量配置被 `is_star` 拒绝；坏编码使 dim U_S 从 13 降到 1，检查器报红。

## 任务 2 · 搜索与复现
- 1,000 组配置 × 8 窗口 = **8,000 项精确检查**；**0 违例**。
- **1,695** 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对；抽查 **60** 组秩检查，**60/60** 通过。
- 精确复现 Appendix C.2 两条代表行：4×4（P=35、|RZ|=4、dim=13、H2=17）；hex17（P=37、|RZ|=5、dim=13、H2=18）。
- 产物：`artifacts/search-results.csv`、`caseb-rank-results.csv`、`search-summary.json`、`validation-examples.json`、`violations.json`。

## 任务 3 · 验证地图
- `report/verification-map.html` / `.md` / `status-table.csv`：三篇论文 × 23 条作品，状态分级与“还缺什么”。
- 浏览器快照确认 23 条作品、23 个 API 证据链接 + 3 个 PDF 链接可点。

## 任务 4 · 投稿包
- `submission.md`：标题 84 字符、正文 10,236 字符；`check_submission.py --allow-placeholder` PASS。
- `submission-challenge.md`：不适用（未发现反例）。
- `report/SHA256SUMS.txt`：已生成（以清单为准）。
- 数字可追溯：`report/claim-map.csv` 逐项映射到 artifacts，校验全过。

## 任务 5 · 人类闸门
- 待领导本人：建公开仓库 → 替换 `REPO_URL` → 注册/登录 → 粘贴提交（10-29 24:00 前）→ 记录作品 ID。
- 清单：`report/SUBMIT-CHECKLIST.md`。
- 提交后：重跑 `python code/make_manifest.py` 与 `python code/check_submission.py`（不带 `--allow-placeholder`），确认哈希与长度全过。

## 下一步
- 用户 push 后把 `REPO_URL` 替换为真实地址；未发现反例，按 `verification` 投，不改 `challenge`。
