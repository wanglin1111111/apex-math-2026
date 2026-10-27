# Apex Math · 凸 Nivat 附录 C.2 独立精确验证

这是一个独立、从零实现的有限验证仓库，针对 Apex Math 悬赏第三篇论文（凸 Nivat）附录 C.2 的 Experiment 2 家族。没有复制论文或任何投稿的代码。

## 结果

- **8,000 项精确窗口检查**：1,000 组配置 × 8 个 Appendix C.2 窗口。
- **0 违例**：所有检查都满足 Pθ(S) ≥ |S|+1。
- **1,695** 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对。
- **60/60** 组抽样秩检查满足 dim U_S = |S|+1−|RZ(S)| 与 H2(S) = |S|+1。
- 复现论文 Appendix C.2 两条代表行的 Pθ、|RZ|、dim U_S 与 H2（4×4 与 hex17；d 取另一组合法见证）。

## 不是什么

这不是 Theorem T 的证明，不覆盖 Experiment 1、一般星形配置或 m=3 的 Case-B/RZ；论文原始 84+157 组随机运行因脚本/RNG 未提供而无法逐次复现。

## 快速开始

```sh
python code/run_search.py
python code/validation_examples.py
cd code && python -m unittest discover -v
cd .. && python code/negative_controls.py
python code/cross_check.py
python code/build_map.py
python code/check_submission.py --allow-placeholder
```

环境：Python 3.11.9；仅标准库（无任何第三方依赖）；无 Lean；无 pytest（unittest）。

## 文件

- `submission.md`：投稿正文（标题 84 字符，正文 10,236 字符，上限 20,000）。
- `report/report.md`：完整方法、结果、负例红→绿、已知 bug 与限制。
- `report/verification-map.html`：三篇论文 × 23 条作品的验证地图。
- `report/SHA256SUMS.txt`：交付物哈希清单。
- `artifacts/`：论文 PDF、榜单快照、搜索 CSV/JSON、两条代表行 JSON、交叉复核 JSON。
- `code/`：生成器、精确计数、Case A/B、zonotope/RZ、秩检查、测试与负例。

## AI 披露

本仓库在 AI 辅助下完成；投稿人未逐行人工复核全部代码或推导。有限检查、负例和代表行可由上面的命令复跑；这不是人类专家背书。

## 许可

代码与文本以 MIT 许可发布（论文原文版权归原作者）。
