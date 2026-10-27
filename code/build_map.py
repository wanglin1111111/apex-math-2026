"""Build the reader-facing verification map from the 2026-10-27 snapshot."""

from __future__ import annotations

import csv
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"
REPORT = ROOT / "report"
REPORT.mkdir(exist_ok=True)

SNAPSHOT = json.loads((ART / "site-snapshot.json").read_text(encoding="utf-8"))
SUMMARY = json.loads((ART / "search-summary.json").read_text(encoding="utf-8"))

PAPERS = {
    "seifert-surfaces": {
        "title": "Contractibility of the complex of incompressible Seifert surfaces",
        "short": "P1 · Seifert / Kakimizu",
        "pdf": "https://math.apexin.net/papers/seifert-surfaces.pdf",
        "focus": "Theorem A（纽结）、B（交换复形）、C（截断）、D（链接）",
    },
    "curve-complex-genus-two": {
        "title": "The complex of curves pairwise intersecting at most once is contractible in genus two",
        "short": "P2 · Curve complex, genus 2",
        "pdf": "https://math.apexin.net/papers/curve-complex-genus-two.pdf",
        "focus": "C₁(S₂) 可缩；Souto 问题的 genus 2 情形",
    },
    "convex-nivat": {
        "title": "The convex Nivat conjecture",
        "short": "P3 · Convex Nivat",
        "pdf": "https://math.apexin.net/papers/convex-nivat.pdf",
        "focus": "Theorem A（星形配置）、Theorem B（凸 Nivat 归约）",
    },
}

STATUS = {
    10: ("complete-claim", "Theorem B 完整 Lean；A/C/D 明确标注仅条件验证"),
    14: ("audit", "Theorem 5.1 的 87 步逐行审计；作者声明是纸笔审计，不是形式化"),
    19: ("audit", "Theorem A 几何部分 + §6.2 的独立审计，列出六处修补 G1–G6"),
    20: ("audit", "Fin 紧致性与滑动经线边界的独立验证"),
    15: ("supplement", "不动点/等变版本的补充"),
    16: ("repair", "指出并修补紧致性输入缺口；作者声明不是反例"),
    17: ("supplement", "开问题 (F) 的反例 + 环面纽结有限性"),
    21: ("partial", "只做 Hopf 纤维链等部分链接扩展；不主张全链接"),
    23: ("partial", "部分 Lean 形式化，归在 challenge 类；不是具体缺口指控"),
    13: ("complete-claim", "全篇 Lean；作者声称无 sorry/admit，公理审计为标准三条"),
    1: ("audit", "六点 Budget 引理的穷举验证"),
    2: ("audit", "增广谱序列步骤的验证"),
    11: ("partial", "条件 Lean：弧收缩与弧–曲线对应"),
    12: ("partial", "条件 Lean：来自已审经典输入"),
    3: ("supplement", "分层强形变收缩，补强定理 1.1"),
    22: ("supplement", "高阶连通、不动点与等变障碍"),
    18: ("complete-claim", "全篇 Lean；作者声称覆盖 49 个原论文结果；附录 C 原脚本未提供，未声称复跑"),
    4: ("audit", "Theorem A §§0–7 验证；附录 C 解释性错误不影响主线"),
    5: ("audit", "§8 + 附录 D 归约验证；Theorem A 作为输入"),
    6: ("complete-claim", "Theorem B（8.18）完整 Lean；不是全篇"),
    9: ("audit", "Lemma 5.2 商代数核验 + 精确证书"),
    7: ("supplement", "Case B 星形配置的互补复杂度界"),
    8: ("supplement", "scalar bridge 替代谱/背景模块；作者声明不转移附录 C 证书"),
}

BADGE = {
    "complete-claim": ("作者声称完整", "#0f766e"),
    "audit": ("独立审计/复算", "#1d4ed8"),
    "repair": ("缺口修补", "#b45309"),
    "supplement": ("补充/推广", "#6d28d9"),
    "partial": ("部分/条件", "#475569"),
}

ROWS = []
for slug, board in SNAPSHOT["leaderboards"].items():
    for item in board["items"]:
        cid = item["id"]
        status, note = STATUS.get(cid, ("partial", "未分类"))
        ROWS.append(
            {
                "paper": slug,
                "paper_short": PAPERS[slug]["short"],
                "id": cid,
                "kind": item["kind"],
                "title": item["title"],
                "author": item["author"]["display_name"],
                "votes": item["vote_count"],
                "created": item["created_at"][:10],
                "status": status,
                "status_label": BADGE[status][0],
                "note": note,
                "evidence": f"https://math.apexin.net/api/v1/challenges/{cid}",
                "pdf": PAPERS[slug]["pdf"],
            }
        )

ROWS.sort(key=lambda r: (list(PAPERS).index(r["paper"]), r["id"]))

WHAT_REMAINS = [
    ("P1", "重大漏洞类没有真正的缺口/反例条目。",
     "Theorem D 没有独立的无条件验证：#10 只做条件形式化，#19 只读了链接部分，#21 只覆盖 Hopf 子类。"),
    ("P2", "重大漏洞类没有真正的缺口/反例条目。",
     "论文自己说明方法不外推到 g ≥ 3；带 puncture/边界的情形也未处理。"),
    ("P3", "重大漏洞类没有真正的缺口/反例条目。",
     "附录 C 的 star.py/verify.py 未随 PDF/公开 Math-Paper 仓库提供；#18 明确说原脚本没有复现。"),
    ("全局", "23 条里没有一条是“给出具体反例/具体失效步骤”的 challenge。",
     "唯一 kind=challenge 的 #23 是部分 Lean 形式化，不是缺口指控。"),
]

CHECK = {
    "configs": SUMMARY["configs_generated"],
    "windows": SUMMARY["window_checks"],
    "violations": SUMMARY["violations"],
    "caseb_rz": SUMMARY["caseb_rz_pairs"],
    "rank_checks": SUMMARY["rank_checks"],
    "rank_ok": SUMMARY["rank_ok"],
}

HTML = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Apex Math 候选论证验证地图</title>
<style>
:root {{ --bg:#0b1020; --panel:#141b31; --text:#e8ecf7; --muted:#9aa6c4; --line:#2a3557; --accent:#6ee7ff; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:15px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }}
main {{ max-width:1180px; margin:0 auto; padding:32px 20px 80px; }}
h1 {{ font-size:30px; margin:0 0 8px; letter-spacing:-.02em; }}
h2 {{ font-size:21px; margin:34px 0 12px; }}
h3 {{ font-size:17px; margin:18px 0 8px; }}
p {{ margin:8px 0; }}
a {{ color:var(--accent); text-decoration:none; }}
a:hover {{ text-decoration:underline; }}
.sub {{ color:var(--muted); }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:12px; margin:20px 0; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:14px; }}
.card b {{ display:block; font-size:24px; }}
.card span {{ color:var(--muted); font-size:13px; }}
.warn {{ background:#3a1d1d; border:1px solid #7f1d1d; border-radius:12px; padding:14px 16px; margin:18px 0; }}
.paper {{ background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:18px; margin:16px 0; }}
.paper h3 {{ margin-top:0; }}
table {{ width:100%; border-collapse:collapse; font-size:13.5px; }}
th, td {{ text-align:left; padding:9px 10px; border-top:1px solid var(--line); vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:999px; color:#fff; font-size:12px; white-space:nowrap; }}
.kind {{ color:var(--muted); font-size:12px; }}
.grid {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
@media (max-width:800px) {{ .grid {{ grid-template-columns:1fr; }} }}
ul {{ margin:8px 0 0 18px; padding:0; }}
li {{ margin:6px 0; }}
.footer {{ color:var(--muted); font-size:12px; margin-top:36px; border-top:1px solid var(--line); padding-top:14px; }}
code {{ background:#0a0f1e; border:1px solid var(--line); padding:1px 5px; border-radius:5px; }}
</style>
</head>
<body>
<main>
<h1>Apex Math 候选论证验证地图</h1>
<p class="sub">快照：{html.escape(SNAPSHOT['fetched_at'])} · 数据源：math.apexin.net 公开 API · 本页只做状态标注，不代表主办方评审结论。</p>

<div class="cards">
<div class="card"><b>{len(ROWS)}</b><span>已公开上榜作品</span></div>
<div class="card"><b>{SNAPSHOT['stats']['participant_count']}</b><span>参与者</span></div>
<div class="card"><b>{SNAPSHOT['stats']['vote_count']}</b><span>当前点赞</span></div>
<div class="card"><b>9</b><span>专业奖（3 篇 × 3 类）</span></div>
<div class="card"><b>{CHECK['configs']}×8</b><span>本仓库独立检查（配置×窗口）</span></div>
</div>

<div class="warn">
<b>先说结论：</b>23 条里没有一条是“给出具体反例或具体失效步骤”的重大漏洞条目；唯一 kind=challenge 的 #23 是部分 Lean 形式化。P2/P3 的“全篇 Lean”是作者声称，不是本页独立复核的结论。P3 的附录 C 原脚本未随 PDF/公开 Math-Paper 仓库提供——本仓库的独立检查是另起炉灶的重实现。
</div>

<h2>三篇论文 · 逐条状态</h2>
"""

for slug in PAPERS:
    meta = PAPERS[slug]
    rows = [r for r in ROWS if r["paper"] == slug]
    HTML += f'<section class="paper"><h3>{html.escape(meta["short"])}</h3>'
    HTML += f'<p class="sub">{html.escape(meta["title"])}<br>重点：{html.escape(meta["focus"])} · <a href="{meta["pdf"]}">论文 PDF</a></p>'
    HTML += "<table><thead><tr><th>#</th><th>状态</th><th>作品</th><th>作者/票</th><th>本页备注</th></tr></thead><tbody>"
    for r in rows:
        color = BADGE[r["status"]][1]
        HTML += (
            f'<tr><td><a href="{r["evidence"]}">#{r["id"]}</a></td>'
            f'<td><span class="badge" style="background:{color}">{r["status_label"]}</span><br><span class="kind">{r["kind"]}</span></td>'
            f'<td>{html.escape(r["title"])}</td>'
            f'<td class="sub">{html.escape(r["author"])}<br>{r["votes"]} 票 · {r["created"]}</td>'
            f'<td>{html.escape(r["note"])}</td></tr>'
        )
    HTML += "</tbody></table></section>"

HTML += "<h2>还缺什么</h2><ul>"
for tag, head, detail in WHAT_REMAINS:
    HTML += f"<li><b>{html.escape(tag)}</b>：{html.escape(head)} {html.escape(detail)}</li>"
HTML += "</ul>"

HTML += f"""
<h2>本仓库的独立检查（P3 · Experiment 2 家族）</h2>
<div class="grid">
<div class="card">
<b>{CHECK['windows']}</b><span>精确窗口检查（{CHECK['configs']} 组配置 × 8 窗口）</span>
<p class="sub">Pθ(S) 用精确枚举，不是抽样下界；每组的 Pθ(S) 与 |S|+1 逐项比较。结果：<b>{CHECK['violations']} 违例</b>。</p>
</div>
<div class="card">
<b>{CHECK['rank_ok']}/{CHECK['rank_checks']}</b><span>Case-B / RZ≠∅ 秩检查通过</span>
<p class="sub">共找到 {CHECK['caseb_rz']} 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对；抽查 {CHECK['rank_checks']} 组，dim U_S 与 H2 全部达到论文下界。</p>
</div>
</div>
<p class="sub">复现的论文表格行（p=3，方向 (1,2),(1,0)）：4×4 窗口 Pθ=35、|RZ|=4、dim U_S=13、H2=17；hex17 窗口 Pθ=37、|RZ|=5、dim U_S=13、H2=18。与论文 Appendix C.2 的代表行一致。</p>
<p class="sub">范围与限制：只覆盖 Experiment 2 的 m=2、k=1、常数尾家族；不覆盖 m=3 的 Case-B/RZ（论文自己的生成器也没有产出这类样本），也不构成对 Theorem T 的证明。完整方法、代码、CSV/JSON 与负例红→绿证据见仓库的 <code>report/report.md</code>。</p>

<h2>怎么读这张图</h2>
<ul>
<li><b>作者声称完整</b>：投稿声称完整形式化/验证，但本页没有独立复核其 Lean 仓库或证明文本。</li>
<li><b>独立审计/复算</b>：投稿给出了独立论证或可复跑证书，本页读了正文，但没有逐行复跑全部代码。</li>
<li><b>缺口修补</b>：投稿指出一个缺口并给出修补；它不是“重大漏洞”条目，但说明原论证有薄弱点。</li>
<li><b>补充/推广</b>：在原文结论上做扩展、简化或补充。</li>
<li><b>部分/条件</b>：投稿自己明确限定范围、条件或只完成了一部分。</li>
</ul>

<div class="footer">
生成时间：{html.escape(SNAPSHOT['fetched_at'])}。榜单与票数会变；本页是快照，不是实时状态。所有“已验证/完整”字样都指投稿作者的声明，除非本页明确写了“本仓库独立检查”。本页与投稿均披露 AI 辅助；不声称人类专家背书。
</div>
</main>
</body>
</html>
"""

(REPORT / "verification-map.html").write_text(HTML, encoding="utf-8")

# Markdown companion
md = ["# Apex Math 候选论证验证地图", "", f"快照：{SNAPSHOT['fetched_at']}。数据源：math.apexin.net 公开 API。", "",
      "> 23 条里没有一条是“给出具体反例/具体失效步骤”的重大漏洞条目；唯一 kind=challenge 的 #23 是部分 Lean 形式化。P2/P3 的“全篇 Lean”是作者声称，不是本页独立复核的结论。", ""]
for slug in PAPERS:
    meta = PAPERS[slug]
    md += [f"## {meta['short']}", "", f"{meta['title']}", "", f"重点：{meta['focus']} · [论文 PDF]({meta['pdf']})", "",
           "| # | 状态 | 作品 | 作者/票 | 本页备注 |", "|---|---|---|---|---|"]
    for r in [x for x in ROWS if x["paper"] == slug]:
        md.append(f"| [#{r['id']}]({r['evidence']}) | {r['status_label']} | {r['title']} | {r['author']} / {r['votes']} | {r['note']} |")
    md.append("")
md += ["## 还缺什么", ""]
for tag, head, detail in WHAT_REMAINS:
    md.append(f"- **{tag}**：{head} {detail}")
md += ["", "## 本仓库的独立检查（P3 · Experiment 2 家族）", "",
       f"- {CHECK['configs']} 组配置 × 8 窗口 = {CHECK['windows']} 项精确检查；违例 {CHECK['violations']}。",
       f"- 找到 {CHECK['caseb_rz']} 组 Case-B 且 RZ(S)≠∅ 的配置–窗口对；抽查 {CHECK['rank_checks']} 组，{CHECK['rank_ok']}/{CHECK['rank_checks']} 通过。",
       "- 复现论文代表行：4×4 窗口 Pθ=35、|RZ|=4、dim U_S=13、H2=17；hex17 窗口 Pθ=37、|RZ|=5、dim U_S=13、H2=18。",
       "- 范围：只覆盖 Experiment 2 的 m=2、k=1、常数尾家族；不覆盖 m=3 的 Case-B/RZ，也不构成对 Theorem T 的证明。", ""]
(REPORT / "verification-map.md").write_text("\n".join(md), encoding="utf-8")

with (REPORT / "status-table.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(ROWS[0].keys()))
    writer.writeheader()
    writer.writerows(ROWS)
(ART / "map-data.json").write_text(json.dumps(ROWS, ensure_ascii=False, indent=1), encoding="utf-8")

print("entries", len(ROWS))
print("html", REPORT / "verification-map.html")
print("md", REPORT / "verification-map.md")
