#!/usr/bin/env python3
"""
构建采薇去重索引

输出 3 个轻量文件，替代 agent 读取 ~993KB 原始数据：

  pipeline/baseline_names.jsonl    — 基线数据集名称（供小蜜蜂查阅，~10KB）
  pipeline/reported_names.jsonl    — 已在报告中介绍过的数据集名称（供语教授去重，~10KB）
  pipeline/dataset_urls.json       — 名称→URL 映射（供报告生成时查链接，~35KB）

用法:
  python3 scripts/build_dedup_index.py [--full|--incremental]
  --full         重建完整索引（默认）
  --incremental  仅处理上次索引之后的新报告，并合并缓存
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
SOURCES_FILE = WORKSPACE / "bee_sources.json"
REPORTS_DIR = WORKSPACE / "sources_reports"
PIPELINE_DIR = WORKSPACE / "pipeline"
CACHE_FILE = PIPELINE_DIR / "_reported_cache.json"

# Output files
BASELINE_NAMES = PIPELINE_DIR / "baseline_names.jsonl"
REPORTED_NAMES = PIPELINE_DIR / "reported_names.jsonl"
DATASET_URLS = PIPELINE_DIR / "dataset_urls.json"

SKIP_HEADERS = {
    "新增数据集", "更新数据集", "陈旧数据集", "推荐变更",
    "top 10", "top 10 更新建议", "执行摘要", "搜索统计",
    "下次运行", "概述", "时效性分析", "基线健康度",
    "本次变化", "备注", "总结", "建议",
    "多语言数据集寻源增量报告", "增量报告",
    # 论文章节标题（防止论文标题被误识别为数据集名）
    "相关论文", "论文", "references", "参考文献",
    "pipeline 状态", "pipeline status",
}

# 以 emoji 开头的非数据集标题模式
EMOJI_SKIP_PREFIXES = ("🌍", "📊", "📚", "🔧", "📄", "⭐", "🏆", "🚨", "💡", "📋")


def normalize_name(name):
    name = re.sub(r"^\d+(\.\d+)*\.?\s+", "", name)
    name = re.sub(r"^[⚠️🔄🗑️🆕⭐️✅❌\s]+", "", name)
    name = re.sub(r"（[^）]+）$", "", name)
    return name.strip()


def is_dataset_header(name):
    lower = name.lower().strip()
    if lower in SKIP_HEADERS:
        return False
    if len(lower) < 2:
        return False
    if re.match(r"^(概述|时效|基线|本次|备注|总结|建议|搜索|下次|top|round)", lower):
        return False
    # 跳过以 emoji 开头的非数据集标题（论文、统计等章节）
    if any(name.startswith(p) for p in EMOJI_SKIP_PREFIXES):
        return False
    return True


def load_sources():
    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = {}
    for src in data.get("sources", []):
        name = src.get("name", "").strip()
        if not name:
            continue
        key = normalize_name(name).lower()
        entries[key] = {"name": name, "url": src.get("url", "")}
    return entries


def extract_from_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    report_date = report_path.stem
    datasets = []
    sections = re.split(r"^## ", content, flags=re.MULTILINE)

    for section in sections:
        first_line = section.split("\n")[0].strip().lower()
        is_dataset_section = any(
            kw in first_line for kw in ["新增数据集", "更新数据集", "陈旧数据集"]
        )
        if not is_dataset_section and "**链接**" not in section:
            continue

        headers = re.findall(r"^###\s+(.+?)$", section, re.MULTILINE)
        urls = re.findall(r"\*\*链接\*\*:\s*(https?://\S+)", section)

        for i, header in enumerate(headers):
            name = normalize_name(header)
            if not is_dataset_header(name):
                continue
            # 跳过包含描述性后缀的条目（版本更新说明、状态标注等）
            if re.search(r"(—\s*\d{4}-|（[^）]*更新|（[^）]*升级|（[^）]*扩展|版本更新|首次跟踪|状态升级)", name):
                continue
            url = urls[i] if i < len(urls) else ""
            datasets.append({"name": name, "url": url})

    return {"report_date": report_date, "datasets": datasets}


def load_cache():
    """Load cached report data for incremental mode."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_indexed_report": None, "reported": {}}


def save_cache(last_report, reported):
    """Save cache for next incremental run."""
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "last_indexed_report": last_report,
            "reported": reported,
        }, f, ensure_ascii=False)


def build_index(mode="full"):
    sources = load_sources()
    print(f"Baseline: {len(sources)} sources")

    report_files = sorted(REPORTS_DIR.glob("*.md"))

    # In incremental mode, start from cache and only process new reports
    reported = {}  # key -> {name, url, dates: []}
    if mode == "incremental":
        cache = load_cache()
        last_indexed = cache.get("last_indexed_report")
        reported = cache.get("reported", {})
        if last_indexed:
            print(f"Incremental: starting from cached state ({len(reported)} entries, last: {last_indexed})")
            # Filter to only new reports
            report_files = [rf for rf in report_files if rf.stem > last_indexed]
            print(f"Incremental: {len(report_files)} new reports to process")
    else:
        print("Full rebuild: processing all reports")

    new_datasets = 0
    for rf in report_files:
        report_date = rf.stem
        extracted = extract_from_report(rf)
        for ds in extracted["datasets"]:
            key = normalize_name(ds["name"]).lower()
            if key in reported:
                if report_date not in reported[key].get("dates", []):
                    reported[key]["dates"].append(report_date)
                if ds.get("url") and not reported[key].get("url"):
                    reported[key]["url"] = ds["url"]
            else:
                new_datasets += 1
                reported[key] = {
                    "name": ds["name"],
                    "url": ds.get("url", ""),
                    "dates": [report_date],
                }

    print(f"After processing: {len(reported)} unique reported datasets (+{new_datasets} new)")

    # Build URL map
    url_map = {}
    for key, src in sources.items():
        if src.get("url"):
            url_map[key] = src["url"]
    for key, rep in reported.items():
        if rep.get("url"):
            url_map[key] = rep["url"]

    # === Write output files ===
    os.makedirs(PIPELINE_DIR, exist_ok=True)

    # 1. baseline_names.jsonl
    baseline_names = sorted(
        [src["name"] for src in sources.values()],
        key=lambda x: x.lower()
    )
    with open(BASELINE_NAMES, "w", encoding="utf-8") as f:
        for name in baseline_names:
            f.write(name + "\n")

    # 2. reported_names.jsonl
    reported_names_list = sorted(
        [rep["name"] for rep in reported.values()],
        key=lambda x: x.lower()
    )
    with open(REPORTED_NAMES, "w", encoding="utf-8") as f:
        for name in reported_names_list:
            f.write(name + "\n")

    # 3. dataset_urls.json
    urls_compact = {}
    for key, url in sorted(url_map.items()):
        if url:
            orig_name = sources.get(key, reported.get(key, {})).get("name", key)
            urls_compact[orig_name] = url
    with open(DATASET_URLS, "w", encoding="utf-8") as f:
        json.dump(urls_compact, f, ensure_ascii=False, separators=(",", ":"))

    # Save cache for next incremental run
    last_report = sorted(REPORTS_DIR.glob("*.md"))
    last_report_name = last_report[-1].stem if last_report else None
    save_cache(last_report_name, reported)

    # Stats
    bl_size = os.path.getsize(BASELINE_NAMES)
    rp_size = os.path.getsize(REPORTED_NAMES)
    url_size = os.path.getsize(DATASET_URLS)
    total_new = bl_size + rp_size + url_size

    print(f"\n=== Output Files ===")
    print(f"  baseline_names.jsonl:  {len(baseline_names):>4} names,  {bl_size:>6,} bytes")
    print(f"  reported_names.jsonl:  {len(reported_names_list):>4} names,  {rp_size:>6,} bytes")
    print(f"  dataset_urls.json:     {len(urls_compact):>4} urls,   {url_size:>6,} bytes")
    print(f"  Total:                                {total_new:>6,} bytes ({total_new/1024:.0f}KB)")
    print(f"\n=== Token Savings ===")
    print(f"  Before: ~993KB (bee_sources.json 337KB + reports 656KB)")
    print(f"  After:  ~{total_new/1024:.0f}KB")
    print(f"  Reduction: {100 - total_new/993000*100:.1f}%")
    print(f"\n  小蜜蜂 reads: baseline_names.jsonl ({bl_size/1024:.0f}KB) instead of bee_sources.json (337KB)")
    print(f"  语教授 reads: reported_names.jsonl ({rp_size/1024:.0f}KB) instead of all reports (656KB)")


if __name__ == "__main__":
    mode = "incremental" if "--incremental" in sys.argv else "full"
    build_index(mode)
    print("\nDone ✅")
