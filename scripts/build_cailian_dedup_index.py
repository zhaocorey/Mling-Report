#!/usr/bin/env python3
"""
构建采莲去重索引

输出 3 个轻量文件，替代 agent 读取 ~561KB 原始数据：

  pipeline/cailian_baseline_names.jsonl  — 基线论文/工具/博客名称（供小蜜蜂查阅，~8KB）
  pipeline/cailian_reported_names.jsonl   — 已在报告中介绍过的名称（供语教授去重，~8KB）
  pipeline/cailian_urls.json             — 名称→URL 映射（~15KB）

用法:
  python3 scripts/build_cailian_dedup_index.py [--full|--incremental]
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
BASELINE_FILE = WORKSPACE / "pipeline" / "bee_dataset_filtering_research.json"
REPORTS_DIR = WORKSPACE / "dataset_filtering_survey"
PIPELINE_DIR = WORKSPACE / "pipeline"
CACHE_FILE = PIPELINE_DIR / "_cailian_reported_cache.json"

# Output files
BASELINE_NAMES = PIPELINE_DIR / "cailian_baseline_names.jsonl"
REPORTED_NAMES = PIPELINE_DIR / "cailian_reported_names.jsonl"
URLS_FILE = PIPELINE_DIR / "cailian_urls.json"

# Section headers that are NOT paper/tool/blog titles
SKIP_HEADERS = {
    "新增论文", "新增工具/仓库", "新增博客/教程", "更新内容",
    "趋势洞察", "建议", "概览", "搜索覆盖", "扫描详情",
    "累计基线状态", "立即行动", "重点跟进", "中长期跟踪",
    "综合行动建议", "发表渠道分布",
}


def normalize(name):
    """Normalize a title for dedup matching."""
    # Strip leading numbering: "1. ", "2. "
    name = re.sub(r"^\d+(\.\d+)*\.?\s*", "", name)
    # Strip emoji prefixes
    name = re.sub(r"^[📂🆕🔄🗑️⭐️✅❌⚠️📈💡🔧📝🚀\s]+", "", name)
    # Strip markdown links: [Title](url) → Title
    name = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", name)
    # Strip trailing parenthetical annotations like （详见 xxx.md）
    name = re.sub(r"（[^）]*）$", "", name)
    # Strip trailing "— xx篇" annotations
    name = re.sub(r"\s*—\s*\d+\s*篇.*$", "", name)
    return name.strip()


def is_real_title(name):
    """Check if a ### header is a real paper/tool/blog title (not a section header)."""
    lower = name.lower().strip()
    if not lower or len(lower) < 3:
        return False
    # Skip common section headers
    for skip in SKIP_HEADERS:
        if lower.startswith(skip.lower()):
            return False
    # Skip date-only or meta headers
    if re.match(r"^(jul|jun|aug|sep|oct|nov|dec|jan|feb|mar|apr|may)\s+\d+", lower):
        return False
    if re.match(r"^(\d{4}-\d{2}-\d{2}|p0|p1|p2)", lower):
        return False
    return True


def load_baseline():
    """Load baseline JSON and extract names + URLs."""
    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    papers = {}
    for p in data.get("papers", []):
        title = (p.get("title") or "").strip()
        if title:
            key = normalize(title).lower()
            papers[key] = {
                "name": title,
                "url": p.get("url") or p.get("arxiv_url") or p.get("link") or "",
                "type": "paper",
            }

    tools = {}
    for t in data.get("tools_and_repos", []):
        name = (t.get("name") or "").strip()
        if name:
            key = normalize(name).lower()
            tools[key] = {
                "name": name,
                "url": t.get("url") or t.get("github_url") or t.get("link") or "",
                "type": "tool",
            }

    blogs = {}
    for b in data.get("blog_posts_and_tutorials", []):
        title = (b.get("title") or "").strip()
        if title:
            key = normalize(title).lower()
            blogs[key] = {
                "name": title,
                "url": b.get("url") or b.get("link") or "",
                "type": "blog",
            }

    return papers, tools, blogs


def extract_from_report(report_path):
    """Extract paper/tool/blog titles and URLs from a report."""
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    report_date = report_path.stem
    papers = []
    tools = []
    blogs = []

    # Split by ## sections to identify category
    sections = re.split(r"^## ", content, flags=re.MULTILINE)

    for section in sections:
        first_line = section.split("\n")[0].strip().lower()

        # Determine category
        is_paper = "论文" in first_line and "新增" in first_line
        is_tool = "工具" in first_line or "仓库" in first_line
        is_blog = "博客" in first_line or "教程" in first_line

        if not (is_paper or is_tool or is_blog):
            # Also check for content with links
            if "**链接**" not in section and "arxiv" not in section.lower():
                continue

        # Extract ### headers
        headers = re.findall(r"^###\s+(.+?)$", section, re.MULTILINE)
        # Extract URLs (multiple patterns)
        urls = re.findall(r"\*\*链接\*\*:\s*(https?://\S+)", section)
        urls += re.findall(r"\*\*(?:arXiv|GitHub|链接|URL)\*\*:\s*(https?://\S+)", section)
        # Also match bare arxiv/github URLs after titles
        arxiv_urls = re.findall(r"(https?://arxiv\.org/abs/\S+)", section)
        github_urls = re.findall(r"(https?://github\.com/\S+)", section)

        all_urls = urls + arxiv_urls + github_urls
        # Deduplicate while preserving order
        seen = set()
        unique_urls = []
        for u in all_urls:
            u_clean = u.rstrip(".,)")
            if u_clean not in seen:
                seen.add(u_clean)
                unique_urls.append(u_clean)

        for i, header in enumerate(headers):
            name = normalize(header)
            if not is_real_title(name):
                continue

            url = unique_urls[i] if i < len(unique_urls) else ""

            if is_paper:
                papers.append({"name": name, "url": url})
            elif is_tool:
                tools.append({"name": name, "url": url})
            elif is_blog:
                blogs.append({"name": name, "url": url})
            else:
                # Try to guess from URL
                if "arxiv" in url:
                    papers.append({"name": name, "url": url})
                elif "github" in url:
                    tools.append({"name": name, "url": url})
                else:
                    papers.append({"name": name, "url": url})

    return {
        "report_date": report_date,
        "papers": papers,
        "tools": tools,
        "blogs": blogs,
    }


def load_cache():
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_indexed_report": None, "reported": {}}


def save_cache(last_report, reported):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_indexed_report": last_report,
            "reported": reported,
        }, f, ensure_ascii=False)


def build_index(mode="full"):
    # Step 1: Load baseline
    bl_papers, bl_tools, bl_blogs = load_baseline()
    print(f"Baseline: {len(bl_papers)} papers, {len(bl_tools)} tools, {len(bl_blogs)} blogs")

    # Step 2: Process reports
    report_files = sorted(REPORTS_DIR.glob("*.md"))

    reported = {}  # key -> {name, url, type, dates: []}

    if mode == "incremental":
        cache = load_cache()
        last_indexed = cache.get("last_indexed_report")
        reported = cache.get("reported", {})
        if last_indexed:
            print(f"Incremental: cached {len(reported)} entries, last: {last_indexed}")
            report_files = [rf for rf in report_files if rf.stem > last_indexed]
            print(f"Incremental: {len(report_files)} new reports")

    new_count = 0
    for rf in report_files:
        report_date = rf.stem
        extracted = extract_from_report(rf)

        for item_type, items in [("paper", extracted["papers"]),
                                  ("tool", extracted["tools"]),
                                  ("blog", extracted["blogs"])]:
            for item in items:
                key = normalize(item["name"]).lower()
                if key in reported:
                    if report_date not in reported[key].get("dates", []):
                        reported[key]["dates"].append(report_date)
                    if item.get("url") and not reported[key].get("url"):
                        reported[key]["url"] = item["url"]
                else:
                    new_count += 1
                    reported[key] = {
                        "name": item["name"],
                        "url": item.get("url", ""),
                        "type": item_type,
                        "dates": [report_date],
                    }

    print(f"Reported: {len(reported)} unique entries (+{new_count} new)")

    # Step 3: Build URL map (merge baseline + reports, skip placeholder URLs)
    url_map = {}
    for src in [bl_papers, bl_tools, bl_blogs]:
        for key, item in src.items():
            url = item.get("url", "")
            if url and "xxxxx" not in url and "example" not in url:
                url_map[item["name"]] = url
    for key, item in reported.items():
        url = item.get("url", "")
        if url and "xxxxx" not in url and "example" not in url:
            url_map[item["name"]] = url

    # Step 4: Write output files
    os.makedirs(PIPELINE_DIR, exist_ok=True)

    # baseline_names.jsonl — all names from baseline, one per line, prefixed with type
    baseline_entries = []
    for item in bl_papers.values():
        baseline_entries.append(f"paper\t{item['name']}")
    for item in bl_tools.values():
        baseline_entries.append(f"tool\t{item['name']}")
    for item in bl_blogs.values():
        baseline_entries.append(f"blog\t{item['name']}")
    baseline_entries.sort(key=lambda x: x.lower())

    with open(BASELINE_NAMES, "w", encoding="utf-8") as f:
        for entry in baseline_entries:
            f.write(entry + "\n")

    # reported_names.jsonl — all names from reports, one per line, prefixed with type
    reported_entries = []
    for key, item in reported.items():
        reported_entries.append(f"{item.get('type','?')}\t{item['name']}")
    reported_entries.sort(key=lambda x: x.lower())

    with open(REPORTED_NAMES, "w", encoding="utf-8") as f:
        for entry in reported_entries:
            f.write(entry + "\n")

    # urls.json
    with open(URLS_FILE, "w", encoding="utf-8") as f:
        json.dump(url_map, f, ensure_ascii=False, separators=(",", ":"))

    # Save cache
    last_report = sorted(REPORTS_DIR.glob("*.md"))
    last_report_name = last_report[-1].stem if last_report else None
    save_cache(last_report_name, reported)

    # Stats
    bl_size = os.path.getsize(BASELINE_NAMES)
    rp_size = os.path.getsize(REPORTED_NAMES)
    url_size = os.path.getsize(URLS_FILE)
    total_new = bl_size + rp_size + url_size
    orig_total = 189349 + 372000  # baseline JSON + reports dir

    print(f"\n=== Output Files ===")
    print(f"  cailian_baseline_names.jsonl: {len(baseline_entries):>4} names,  {bl_size:>6,} bytes")
    print(f"  cailian_reported_names.jsonl: {len(reported_entries):>4} names,  {rp_size:>6,} bytes")
    print(f"  cailian_urls.json:            {len(url_map):>4} urls,   {url_size:>6,} bytes")
    print(f"  Total:                                       {total_new:>6,} bytes ({total_new/1024:.0f}KB)")
    print(f"\n=== Token Savings ===")
    print(f"  Before: ~{orig_total/1024:.0f}KB (baseline 185KB + reports 363KB)")
    print(f"  After:  ~{total_new/1024:.0f}KB")
    print(f"  Reduction: {100 - total_new/orig_total*100:.1f}%")
    print(f"\n  小蜜蜂 reads: baseline_names ({bl_size/1024:.0f}KB) instead of baseline JSON (185KB)")
    print(f"  语教授 reads: reported_names ({rp_size/1024:.0f}KB) instead of all reports (363KB)")


if __name__ == "__main__":
    mode = "incremental" if "--incremental" in sys.argv else "full"
    build_index(mode)
    print("\nDone ✅")
