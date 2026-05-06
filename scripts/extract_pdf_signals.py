#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


CATEGORY_PATTERNS: dict[str, list[str]] = {
    "reasoning topology": [
        r"reasoning topology",
        r"reasoning-answer",
        r"hallucination detection",
        r"uncertainty propagation",
        r"conformal prediction",
        r"llm agent",
    ],
    "reasoning graph analysis": [
        r"causal cot graph",
        r"reasoning graph",
        r"computational graph",
        r"attribution graph",
        r"graph-based analysis of reasoning",
        r"belief propagation",
    ],
    "long-form graph UQ": [
        r"long-form generation",
        r"claim level",
        r"entailment graph",
        r"graph-assisted uncertainty",
        r"structural entropy",
    ],
    "long-form calibration": [
        r"long-form",
        r"calibration",
        r"self-correction",
        r"confidence calibration",
    ],
    "sample-efficient": [
        r"single-sequence",
        r"sample-efficient",
        r"few samples",
        r"hedge-to-verify",
    ],
    "uncertainty expression": [
        r"say.?i don.?t know",
        r"uncertainty expression",
        r"risk-controlled refusal",
        r"truth-aligned",
    ],
}


def require_binary(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"missing required binary: {name}")


def run(args: list[str]) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_pdfinfo(raw: str) -> dict[str, str]:
    info: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        info[key.strip()] = value.strip()
    return info


def infer_title(first_page_text: str) -> str | None:
    lines = [normalize_space(line) for line in first_page_text.splitlines()]
    lines = [line for line in lines if line]
    if not lines:
        return None
    skip_re = re.compile(r"^(arxiv:|published as|proceedings of|page\s+\d+)", re.IGNORECASE)
    for line in lines[:10]:
        if skip_re.match(line):
            continue
        if "@" in line or "http" in line.lower():
            continue
        if len(re.findall(r"[A-Za-z][A-Za-z'/-]+", line)) >= 4:
            return line
    return lines[0]


def extract_abstract_excerpt(text: str) -> str | None:
    match = re.search(r"\babstract\b(.*?)(\b1\b\s+introduction|\bintroduction\b)", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    excerpt = normalize_space(match.group(1))
    return excerpt[:1200] if excerpt else None


def count_pattern_hits(text: str) -> dict[str, dict[str, object]]:
    lowered = text.lower()
    results: dict[str, dict[str, object]] = {}
    for category, patterns in CATEGORY_PATTERNS.items():
        hits = [pattern for pattern in patterns if re.search(pattern, lowered, re.IGNORECASE)]
        results[category] = {"hit_count": len(hits), "matched_patterns": hits}
    return results


def infer_year(info: dict[str, str], text: str, file_name: str) -> str | None:
    for candidate in (info.get("CreationDate", ""), text, file_name):
        match = re.search(r"(20\d{2})", candidate)
        if match:
            return match.group(1)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract title, abstract, and category signals from a PDF.")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--pdf", required=True, help="PDF path relative to root or absolute path")
    parser.add_argument("--pages", type=int, default=3, help="How many leading pages to extract")
    args = parser.parse_args()

    require_binary("pdfinfo")
    require_binary("pdftotext")

    repo_root = Path(args.root).resolve()
    pdf_path = Path(args.pdf)
    if not pdf_path.is_absolute():
        pdf_path = repo_root / pdf_path
    if not pdf_path.exists():
        raise SystemExit(f"pdf does not exist: {pdf_path}")

    info = parse_pdfinfo(run(["pdfinfo", str(pdf_path)]))
    page_one = run(["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf_path), "-"])
    leading_text = run(
        ["pdftotext", "-f", "1", "-l", str(args.pages), "-layout", str(pdf_path), "-"]
    )

    title = info.get("Title") or infer_title(page_one)
    abstract_excerpt = extract_abstract_excerpt(leading_text)
    category_hits = count_pattern_hits(f"{title or ''}\n{leading_text}")

    payload = {
        "pdf": str(pdf_path.relative_to(repo_root)) if pdf_path.is_relative_to(repo_root) else str(pdf_path),
        "pages": info.get("Pages"),
        "title": title,
        "author": info.get("Author") or None,
        "year_guess": infer_year(info, leading_text, pdf_path.name),
        "abstract_excerpt": abstract_excerpt,
        "category_signals": category_hits,
        "first_page_excerpt": normalize_space(" ".join(page_one.splitlines()[:20]))[:1200],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
