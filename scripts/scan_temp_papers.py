#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"missing required binary: {name}")


def run(args: list[str]) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout


def parse_pdfinfo(raw: str) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def infer_title(first_page_text: str) -> str | None:
    lines = [normalize_space(line) for line in first_page_text.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return None

    skip_prefixes = (
        "arxiv:",
        "published as",
        "proceedings of",
        "page ",
        "figure ",
        "table ",
    )
    institution_re = re.compile(
        r"\b(university|department|school|institute|laboratory|lab|college|center)\b",
        re.IGNORECASE,
    )
    kept: list[str] = []
    for line in lines[:20]:
        low = line.lower()
        if low.startswith("abstract"):
            break
        if any(low.startswith(prefix) for prefix in skip_prefixes):
            continue
        if "@" in line or "http" in low:
            continue
        kept.append(line)
    if not kept:
        return None

    word_re = re.compile(r"[A-Za-z][A-Za-z'/-]+")
    for idx, line in enumerate(kept[:8]):
        if len(word_re.findall(line)) < 4:
            continue
        title = line
        if idx + 1 < len(kept[:8]):
            nxt = kept[idx + 1]
            if (
                len(word_re.findall(nxt)) >= 3
                and "@" not in nxt
                and not institution_re.search(nxt)
            ):
                title = f"{title} {nxt}"
        return title
    return kept[0]


def infer_year(info: dict[str, str], text: str, file_name: str) -> str | None:
    for candidate in (info.get("CreationDate", ""), text, file_name):
        match = re.search(r"(20\d{2})", candidate)
        if match:
            return match.group(1)
    return None


def first_page_text(pdf_path: Path) -> str:
    return run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf_path), "-"])


def scan_pdf(pdf_path: Path, repo_root: Path) -> dict[str, object]:
    info = parse_pdfinfo(run(["pdfinfo", str(pdf_path)]))
    page_text = first_page_text(pdf_path)
    metadata_title = info.get("Title") or None
    metadata_author = info.get("Author") or None
    inferred_title = infer_title(page_text)
    title = metadata_title if metadata_title else inferred_title
    title_source = "metadata" if metadata_title else ("first_page" if inferred_title else "unknown")

    excerpt_lines = [normalize_space(line) for line in page_text.splitlines() if normalize_space(line)]
    excerpt = " ".join(excerpt_lines[:8])

    return {
        "file_name": pdf_path.name,
        "relative_path": str(pdf_path.relative_to(repo_root)),
        "pages": info.get("Pages"),
        "metadata_title": metadata_title,
        "metadata_author": metadata_author,
        "title": title,
        "title_source": title_source,
        "year_guess": infer_year(info, page_text, pdf_path.name),
        "first_page_excerpt": excerpt,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan paper_reference/temp PDFs and emit a JSON manifest.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--temp-dir", default="paper_reference/temp", help="Temp PDF directory relative to root")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    require_binary("pdfinfo")
    require_binary("pdftotext")

    repo_root = Path(args.root).resolve()
    temp_dir = repo_root / args.temp_dir
    if not temp_dir.exists():
        raise SystemExit(f"temp directory does not exist: {temp_dir}")

    items = [scan_pdf(pdf_path, repo_root) for pdf_path in sorted(temp_dir.glob("*.pdf"))]
    payload = {"count": len(items), "papers": items}
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
