#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


IGNORED_DIRS = {"temp", "datasets"}
IGNORED_FILES = {"INDEX.md", "论文阅读总结模板.md", "研究方向总结.md"}
INDEX_COUNT_RE = re.compile(r"共\s+(\d+)\s+篇")
PDF_LINK_RE = re.compile(r"\[[^\]]*PDF[^\]]*\]\(([^)]+)\)")
CATEGORY_HEADER_RE = re.compile(r"^## (.+)（(\d+)）$")
BULLET_RE = re.compile(r"^- \[[ x]\] \[.+\]\(")


def english_summary_files(category_dir: Path) -> list[Path]:
    files = []
    for path in sorted(category_dir.glob("*.md")):
        if path.name in IGNORED_FILES:
            continue
        if path.name.endswith(" - 中文翻译.md"):
            continue
        files.append(path)
    return files


def indexed_category_dirs(root: Path, categories: list[str]) -> list[Path]:
    paper_root = root / "paper_reference"
    if categories:
        dirs: list[Path] = []
        for name in categories:
            path = paper_root / name
            if not path.exists() or not path.is_dir():
                raise SystemExit(f"category does not exist: {path}")
            dirs.append(path)
        return dirs

    dirs = []
    for path in sorted(paper_root.iterdir()):
        if not path.is_dir() or path.name in IGNORED_DIRS:
            continue
        if english_summary_files(path):
            dirs.append(path)
    return dirs


def extract_pdf_link(summary_path: Path) -> str | None:
    text = summary_path.read_text(encoding="utf-8")
    match = PDF_LINK_RE.search(text)
    if not match:
        return None
    link = match.group(1).strip()
    if link.startswith("<") and link.endswith(">"):
        link = link[1:-1]
    return link


def index_scope_count(index_path: Path, categories: list[str]) -> int | None:
    text = index_path.read_text(encoding="utf-8").splitlines()
    if not categories:
        match = INDEX_COUNT_RE.search("\n".join(text))
        return int(match.group(1)) if match else None

    wanted = set(categories)
    current: str | None = None
    count = 0
    for line in text:
        header = CATEGORY_HEADER_RE.match(line.strip())
        if header:
            current = header.group(1)
            continue
        if current in wanted and BULLET_RE.match(line.strip()):
            count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify paper_reference archive consistency.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument(
        "--category",
        action="append",
        default=[],
        help="Restrict verification to one or more touched categories under paper_reference",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    paper_root = root / "paper_reference"
    errors: list[str] = []
    checked = 0

    temp_dir = paper_root / "temp"
    temp_files = sorted(temp_dir.glob("*")) if temp_dir.exists() else []
    if temp_files:
        errors.append(f"paper_reference/temp is not empty: {len(temp_files)} file(s)")

    total_summaries = 0
    for category_dir in indexed_category_dirs(root, args.category):
        total_summaries += len(english_summary_files(category_dir))
        summary_path = category_dir / "研究方向总结.md"
        if not summary_path.exists():
            errors.append(f"missing category summary: {summary_path}")

        for summary in english_summary_files(category_dir):
            checked += 1
            translation = summary.with_name(f"{summary.stem} - 中文翻译.md")
            if not translation.exists():
                errors.append(f"missing translation for {summary}")

            pdf_link = extract_pdf_link(summary)
            if not pdf_link:
                errors.append(f"missing PDF link in {summary}")
                continue
            if "../temp/" in pdf_link:
                errors.append(f"stale temp PDF link in {summary}: {pdf_link}")
            pdf_path = (summary.parent / pdf_link).resolve()
            if not pdf_path.exists():
                errors.append(f"linked PDF does not exist for {summary}: {pdf_link}")

    index_path = paper_root / "INDEX.md"
    if not index_path.exists():
        errors.append(f"missing index: {index_path}")
    else:
        text = index_path.read_text(encoding="utf-8")
        indexed_total = index_scope_count(index_path, args.category)
        if indexed_total is None:
            errors.append("could not find matching count in paper_reference/INDEX.md")
        elif indexed_total != total_summaries:
            scope = ", ".join(args.category) if args.category else "all indexed categories"
            errors.append(
                f"index count mismatch for {scope}: INDEX says {indexed_total}, actual English summaries are {total_summaries}"
            )

    if errors:
        print("archive verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"archive verification passed: checked {checked} paper summaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
