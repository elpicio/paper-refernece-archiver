#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PREFERRED_ORDER = [
    "atomic factuality",
    "SE",
    "benchmark",
    "long-form calibration",
    "long-form fine-grained UQ",
    "long-form graph UQ",
    "long-form benchmark",
    "reasoning graph analysis",
    "reasoning topology",
    "sample-efficient",
    "survey",
    "uncertainty expression",
]
IGNORED_DIRS = {"temp", "datasets"}
IGNORED_FILES = {"INDEX.md", "论文阅读总结模板.md", "研究方向总结.md"}
STATUS_RE = re.compile(r"^- \[([ x])\] \[(.+?)\]\(")
CATEGORY_RE = re.compile(r"^## (.+)（(\d+)）$")


def summary_files(category_dir: Path) -> list[Path]:
    files = []
    for path in sorted(category_dir.glob("*.md")):
        if path.name in IGNORED_FILES:
            continue
        if path.name.endswith(" - 中文翻译.md"):
            continue
        files.append(path)
    return files


def parse_existing_index(index_path: Path) -> tuple[dict[str, str], dict[str, list[str]]]:
    statuses: dict[str, str] = {}
    order_by_category: dict[str, list[str]] = {}
    current_category: str | None = None

    if not index_path.exists():
        return statuses, order_by_category

    for line in index_path.read_text(encoding="utf-8").splitlines():
        category_match = CATEGORY_RE.match(line.strip())
        if category_match:
            current_category = category_match.group(1)
            order_by_category.setdefault(current_category, [])
            continue
        paper_match = STATUS_RE.match(line.strip())
        if paper_match and current_category:
            status = paper_match.group(1)
            title = paper_match.group(2)
            statuses[title] = status
            order_by_category.setdefault(current_category, []).append(title)
    return statuses, order_by_category


def category_dirs(root: Path) -> list[Path]:
    paper_root = root / "paper_reference"
    candidates = [path for path in paper_root.iterdir() if path.is_dir() and path.name not in IGNORED_DIRS]
    dirs = [path for path in candidates if summary_files(path)]
    preferred = [paper_root / name for name in PREFERRED_ORDER if (paper_root / name) in dirs]
    extras = sorted([path for path in dirs if path not in preferred], key=lambda item: item.name.casefold())
    return preferred + extras


def ordered_titles(category: str, files: list[Path], existing_order: dict[str, list[str]]) -> list[str]:
    titles = [path.stem for path in files]
    previous = existing_order.get(category, [])
    kept = [title for title in previous if title in titles]
    new_titles = sorted([title for title in titles if title not in kept], key=str.casefold)
    return kept + new_titles


def render_index(root: Path) -> str:
    paper_root = root / "paper_reference"
    index_path = paper_root / "INDEX.md"
    statuses, existing_order = parse_existing_index(index_path)

    categories = category_dirs(root)
    total = sum(len(summary_files(category_dir)) for category_dir in categories)
    lines = [
        "# Paper Index",
        "",
        f"说明：把 `[ ]` 改成 `[x]` 表示已读。分组名就是分类，共 {total} 篇。",
        "",
    ]

    for category_dir in categories:
        files = summary_files(category_dir)
        titles = ordered_titles(category_dir.name, files, existing_order)
        file_map = {path.stem: path for path in files}
        lines.append(f"## {category_dir.name}（{len(files)}）")
        for title in titles:
            status = statuses.get(title, " ")
            link = f"<./{category_dir.name}/{file_map[title].name}>"
            lines.append(f"- [{status}] [{title}]({link})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate paper_reference/INDEX.md from category directories.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--stdout", action="store_true", help="Print generated index instead of writing it")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paper_root = root / "paper_reference"
    if not paper_root.exists():
        raise SystemExit(f"paper_reference does not exist: {paper_root}")

    content = render_index(root)
    if args.stdout:
        print(content, end="")
        return 0

    index_path = paper_root / "INDEX.md"
    index_path.write_text(content, encoding="utf-8")
    print(f"updated {index_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
