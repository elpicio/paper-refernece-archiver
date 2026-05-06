# Workflow

Script paths in this document are relative to the skill directory. Use `--root` to point them at the repository whose `paper_reference` archive is being updated.

## 1. Inventory

Run:

```bash
python scripts/scan_temp_papers.py --root .
```

This gives a manifest for every PDF in `paper_reference/temp`, including page count, metadata title, inferred title, and a first-page excerpt.

If a paper is ambiguous, run:

```bash
python scripts/extract_pdf_signals.py --root . --pdf paper_reference/temp/<file>.pdf
```

Use the result to inspect:

- title and author quality
- abstract excerpt
- keyword hits
- category signal counts

## 2. Classification

Read `classification-rules.md` before assigning categories.

Decision order:

1. Prefer an existing category if the paper's main contribution clearly fits one.
2. Create a new category only when no existing category fits cleanly and the direction is likely to recur, or the user explicitly asks for a new category.
3. When in doubt between two categories, classify by the paper's main contribution, not by a secondary technique.

## 3. Parallel Writing

If there are at least 3 papers, split paper-level writing across subagents.

Main agent keeps ownership of:

- category structure
- PDF moves
- `paper_reference/INDEX.md`
- category `研究方向总结.md`

Subagents only write:

- `<Title>.md`
- `<Title> - 中文翻译.md`

## 4. Per-Paper Files

For each paper, produce:

- summary file: `<English Title>.md`
- translation file: `<English Title> - 中文翻译.md`
- linked PDF in the same folder

Summary files must follow `paper_reference/论文阅读总结模板.md`.

Translation files should preserve:

- section structure
- formulas
- equation numbers
- algorithm blocks
- important tables and figures

If a very long appendix contains repetitive numeric tables with little explanatory content, it may be summarized briefly, but formulas and methodological details should still be preserved.

## 5. Formula and Table Recovery

When text extraction is damaged:

1. Find the page from `pdftotext` output.
2. Render the page:

```bash
bash scripts/render_pdf_page.sh paper_reference/<category>/<file>.pdf 5
```

3. Inspect the resulting image with vision.
4. Patch the translation file.

This step is required for formula damage such as:

- broken fractions
- missing combinatorics notation
- collapsed super/subscripts
- split equations
- tables with merged columns

## 6. Move PDFs

Only move PDFs after the paper-level files are done.

Keep the original PDF filename unless there is an explicit repo convention to rename it.

## 7. Update Shared Files

Update index with:

```bash
python scripts/update_paper_index.py --root .
```

Then manually update every touched category's `研究方向总结.md`.

If a new category is created, add its own `研究方向总结.md`.

## 8. Verify

Run:

```bash
python scripts/verify_paper_archive.py --root . --category "<touched-category>"
```

Before reporting completion, confirm:

- `paper_reference/temp` is empty or only contains files intentionally left for later
- no summary links still point to `../temp/`
- every new paper has summary, translation, and linked PDF
- `INDEX.md` count matches actual paper count

If the repository already contains older archive inconsistencies outside the current task, restrict verification to the categories you touched.
