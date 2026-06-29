#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from collections import OrderedDict
from html import escape
from pathlib import Path


MODULE_ORDER = [
    "函数与导数",
    "三角函数与解三角形",
    "数列",
    "立体几何与平面向量",
    "解析几何",
    "概率统计与计数原理",
]


def slug_module(index: int, module: str) -> str:
    mapping = {
        "函数与导数": "01_函数与导数",
        "三角函数与解三角形": "02_三角函数与解三角形",
        "数列": "03_数列",
        "立体几何与平面向量": "04_立体几何与平面向量",
        "解析几何": "05_解析几何",
        "概率统计与计数原理": "06_概率统计与计数原理",
    }
    return mapping.get(module, f"{index + 1:02d}_{module}")


def li(items: list[str]) -> str:
    return "\n".join(f"<li>{item}</li>" for item in items)


def read_records(path: Path) -> list[dict]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("question bank must be a JSON list")
    required = {"id", "source", "number", "type", "module", "topic", "title", "question_image", "answer", "key_ideas", "analysis", "warning"}
    for i, record in enumerate(records, 1):
        missing = sorted(required - record.keys())
        if missing:
            raise ValueError(f"record {i} missing fields: {', '.join(missing)}")
    return records


def group_records(records: list[dict]) -> OrderedDict[str, list[dict]]:
    grouped: OrderedDict[str, list[dict]] = OrderedDict()
    for module in MODULE_ORDER:
        values = [r for r in records if r["module"] == module]
        if values:
            grouped[module] = values
    for record in records:
        grouped.setdefault(record["module"], [])
        if record not in grouped[record["module"]]:
            grouped[record["module"]].append(record)
    return grouped


def copy_assets(records: list[dict], input_file: Path, out: Path) -> None:
    for record in records:
        for field in ["question_image"]:
            src = (input_file.parent / record[field]).resolve()
            dst = out / record[field]
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src != dst.resolve():
                shutil.copy2(src, dst)
        for img in record.get("answer_images", []):
            src = (input_file.parent / img).resolve()
            dst = out / img
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src != dst.resolve():
                shutil.copy2(src, dst)


def common_head(title: str, css_href: str) -> str:
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<script>
window.MathJax = {{
  tex: {{ inlineMath: [['\\\\(', '\\\\)'], ['$', '$']], displayMath: [['\\\\[', '\\\\]']] }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<link rel="stylesheet" href="{css_href}">
"""


def write_css(out: Path) -> None:
    (out / "assets").mkdir(exist_ok=True)
    (out / "assets" / "error_book.css").write_text(
        """
:root{--ink:#172033;--muted:#536074;--paper:#fffaf0;--card:#fffef9;--line:#eadcc6;--blue:#245d9b;--blue-soft:#edf5ff;--red:#d82027;--red-soft:#fff0ed;--gold:#b87922}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:linear-gradient(180deg,#f2e6d2 0%,var(--paper) 38%,#f7eedf 100%);font-family:"Songti SC","STSong","Noto Serif CJK SC","PingFang SC","Microsoft YaHei",serif}
header{background:#18365d;color:white;padding:42px 18px 28px;border-bottom:7px solid #d8a24a}.wrap,main{max-width:1120px;margin:0 auto}main{padding:28px 16px 70px}h1{margin:0;font-size:clamp(28px,4vw,44px)}header p{max-width:860px;line-height:1.8;color:#edf5ff}.home-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin-top:22px}
.module-card{display:flex;justify-content:space-between;gap:16px;align-items:center;min-height:150px;padding:22px;color:inherit;text-decoration:none;background:var(--card);border:1px solid var(--line);border-radius:8px;box-shadow:0 12px 28px rgba(72,45,12,.10)}.module-card p,.eyebrow{color:var(--gold);font-weight:900;margin:0 0 6px;font-family:"PingFang SC","Microsoft YaHei",sans-serif}.module-card h2{margin:0 0 10px;font-size:28px}.module-meta{color:var(--muted);line-height:1.7}.module-card span,.home-link,.bottom-nav a,summary{color:white;background:var(--blue);border-radius:999px;padding:9px 14px;text-decoration:none;font-weight:900;font-family:"PingFang SC","Microsoft YaHei",sans-serif}
.home-link{display:inline-block;background:#edf5ff;color:#18365d;margin-bottom:18px}.toc,.bottom-nav{display:flex;flex-wrap:wrap;gap:10px;padding:16px 0 4px}.toc a,.chips a{border:1px solid #b9d3f0;border-radius:999px;background:var(--blue-soft);color:var(--blue);padding:7px 12px;text-decoration:none;font:800 14px/1.2 "PingFang SC","Microsoft YaHei",sans-serif}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:18px 0;padding:22px;box-shadow:0 12px 28px rgba(72,45,12,.10)}.card-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;border-bottom:1px solid #f0e3cf;padding-bottom:14px;margin-bottom:16px}h3{margin:0;font-size:23px}.chips{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;max-width:380px}.question{width:100%;display:block;border:1px solid #eee1cf;border-radius:6px;background:white}.reveal{margin-top:16px;border:1px dashed #d3b37a;border-radius:8px;background:#fffaf0;padding:14px}summary{display:inline-flex;cursor:pointer}summary::marker{content:""}.answer{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center;background:#fff7df;border:1px solid #ead096;border-radius:8px;padding:14px 16px;margin:16px 0}.answer b{background:var(--red);color:white;border-radius:999px;padding:5px 12px}.answer strong{color:var(--red);font-size:21px;line-height:1.55}.key,.solution,.warning{border-radius:8px;padding:16px 18px;margin-top:16px}.key{background:var(--red-soft);border:1px solid #f1b8b1;border-left:7px solid var(--red)}.solution{background:#fbfdff;border:1px solid #d9e8f7}.warning{background:#fff8e8;border:1px solid #ead096}h4{margin:0 0 10px;font-size:18px}li,p{line-height:1.85}.key span,.hi{color:var(--red);font-weight:900}.bottom-nav{border-top:1px solid var(--line);margin-top:24px}
@media(max-width:720px){header .wrap,main{padding-left:12px;padding-right:12px}.home-grid{grid-template-columns:1fr}.module-card,.card-head{display:block}.card{padding:16px 10px}.chips{justify-content:flex-start;margin-top:10px}.answer{grid-template-columns:1fr}}
""".strip(),
        encoding="utf-8",
    )


def analysis_html(record: dict, prefix: str = "") -> str:
    images = "".join(f'<img class="question" src="{prefix}{escape(img)}" alt="答案图">' for img in record.get("answer_images", []))
    if "solution_parts" in record:
        parts = []
        for part in record["solution_parts"]:
            parts.append(f"<section><h4>{part['title']}</h4><ol>{li(part['steps'])}</ol></section>")
        return images + "".join(parts)
    return images + f"<ol>{li(record['analysis'])}</ol>"


def write_home(title: str, groups: OrderedDict[str, list[dict]], out: Path) -> None:
    cards = []
    for index, (module, records) in enumerate(groups.items()):
        topics = "、".join(sorted({r["topic"] for r in records}))
        cards.append(f"""<a class="module-card" href="web_modules/{slug_module(index, module)}.html"><div><p>模块 {index+1}</p><h2>{escape(module)}</h2><div class="module-meta">{len(records)} 道题 · {escape(topics)}</div></div><span>进入练习</span></a>""")
    html = f"""<!doctype html><html lang="zh-CN"><head>{common_head(title + ' · 网页版', 'assets/error_book.css')}</head><body><header><div class="wrap"><h1>{escape(title)}</h1><p>第一页只显示分类入口，点进某一类后再学习这一类题，降低一次性看到全部题目的压力。</p></div></header><main><section class="home-grid">{''.join(cards)}</section></main></body></html>"""
    (out / f"{title}_网页版.html").write_text(html, encoding="utf-8")


def write_module_pages(title: str, groups: OrderedDict[str, list[dict]], out: Path) -> None:
    module_dir = out / "web_modules"
    module_dir.mkdir(exist_ok=True)
    modules = list(groups.keys())
    for index, module in enumerate(modules):
        records = groups[module]
        cards = []
        for record in records:
            cards.append(f"""<article class="card" id="{escape(record['id'])}"><div class="card-head"><div><p class="eyebrow">{escape(record['source'])} · 第 {escape(str(record['number']))} 题 · {escape(record['type'])}</p><h3>{escape(record['title'])}</h3></div><div class="chips"><a href="#top">{escape(module)}</a><a href="#top">{escape(record['topic'])}</a></div></div><img class="question" src="../{escape(record['question_image'])}" alt="{escape(record['id'])} 题目"><details class="reveal"><summary>展开答案与解析</summary><section class="answer"><b>答案</b><strong>{record['answer']}</strong></section><section class="key"><h4>题眼 / 关键步骤</h4><ol>{li(record['key_ideas'])}</ol></section><section class="solution"><h4>解析过程</h4>{analysis_html(record, '../')}</section><section class="warning"><h4>易错提醒</h4><p>{record['warning']}</p></section></details></article>""")
        toc = "".join(f'<a href="#{escape(r["id"])}">{escape(r["source"])} 第 {escape(str(r["number"]))} 题</a>' for r in records)
        bottom = ['<a href="#top">回到本类顶部</a>', f'<a href="../{title}_网页版.html">返回分类首页</a>']
        if index > 0:
            bottom.append(f'<a href="{slug_module(index-1, modules[index-1])}.html">上一类：{escape(modules[index-1])}</a>')
        if index + 1 < len(modules):
            bottom.append(f'<a href="{slug_module(index+1, modules[index+1])}.html">下一类：{escape(modules[index+1])}</a>')
        html = f"""<!doctype html><html lang="zh-CN"><head>{common_head(module + ' · ' + title, '../assets/error_book.css')}</head><body><header id="top"><div class="wrap"><a class="home-link" href="../{title}_网页版.html">返回分类首页</a><p class="eyebrow">模块 {index+1}</p><h1>{escape(module)}</h1><p>本页只显示这一类题，共 {len(records)} 道。每题先看题目，答案与解析默认折叠。</p><nav class="toc">{toc}</nav></div></header><main>{''.join(cards)}<nav class="bottom-nav">{''.join(bottom)}</nav></main></body></html>"""
        (module_dir / f"{slug_module(index, module)}.html").write_text(html, encoding="utf-8")


def print_html(title: str, module: str, records: list[dict], index: int) -> str:
    q_cards, a_cards = [], []
    for record in records:
        q_cards.append(f"""<article class="print-card"><h3>{escape(record['id'])}　{escape(record['source'])} 第 {escape(str(record['number']))} 题</h3><p class="meta">{escape(record['type'])} / {escape(record['topic'])}</p><img src="../{escape(record['question_image'])}" alt="{escape(record['id'])} 题目"><div class="checkline">订正日期：__________　是否掌握：□ 是　□ 否　错因：________________________</div></article>""")
        a_cards.append(f"""<article class="print-card"><h3>{escape(record['id'])}　答案与解析</h3><p class="answer-text"><b>答案：</b>{record['answer']}</p><h4>题眼 / 关键步骤</h4><ol>{li(record['key_ideas'])}</ol><h4>解析过程</h4>{analysis_html(record, '../')}<h4>易错提醒</h4><p>{record['warning']}</p></article>""")
    css = """*{box-sizing:border-box}body{margin:0;color:#171f2f;background:white;font-family:"Songti SC","STSong","Noto Serif CJK SC",serif}.page{max-width:980px;margin:0 auto;padding:30px 24px}header{border-bottom:3px solid #1f4f85;padding-bottom:16px;margin-bottom:22px}h1{margin:0;font-size:31px}header p{line-height:1.8;color:#4e596b}.part-title{page-break-before:always;background:#1f4f85;color:white;padding:14px 18px;margin:34px 0 18px;border-radius:4px}.first{page-break-before:auto}h2{border-left:6px solid #b87922;padding-left:10px;margin:24px 0 12px}.print-card{border:1px solid #d9d9d9;border-radius:6px;padding:14px;margin:12px 0 18px;page-break-inside:avoid}h3{margin:0 0 6px;font-size:20px}h4{margin:14px 0 6px;font-size:17px;color:#1f4f85}.meta{margin:0 0 10px;color:#666}img{width:100%;display:block;border:1px solid #e6e6e6;border-radius:4px}.checkline{margin-top:12px;color:#555;line-height:1.8}.answer-text{color:#d82027;font-size:18px;font-weight:700}li,p{line-height:1.75}.hi,span{color:#d82027;font-weight:800}@page{size:A4;margin:14mm 12mm}@media print{.page{max-width:none;padding:0}.part-title{border-radius:0}}"""
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{escape(module)} · {escape(title)}专项打印</title><style>{css}</style></head><body><main class="page"><header><h1>{escape(module)}专项练习</h1><p>{escape(title)} · 模块 {index+1} · 共 {len(records)} 道题。前半部分为题目册，后半部分为答案解析册。</p></header><h1 class="part-title first">第一部分：题目册</h1><section><h2>{escape(module)}</h2>{''.join(q_cards)}</section><h1 class="part-title">第二部分：答案解析册</h1><section><h2>{escape(module)}</h2>{''.join(a_cards)}</section></main></body></html>"""


def write_print_modules(title: str, groups: OrderedDict[str, list[dict]], out: Path) -> None:
    print_dir = out / "print_modules"
    print_dir.mkdir(exist_ok=True)
    for index, (module, records) in enumerate(groups.items()):
        (print_dir / f"{slug_module(index, module)}.html").write_text(print_html(title, module, records, index), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--title", default="高中数学错题本")
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    records = read_records(args.input)
    copy_assets(records, args.input, args.output)
    groups = group_records(records)
    write_css(args.output)
    write_home(args.title, groups, args.output)
    write_module_pages(args.title, groups, args.output)
    write_print_modules(args.title, groups, args.output)
    print(f"generated {len(records)} problems in {args.output}")


if __name__ == "__main__":
    main()
