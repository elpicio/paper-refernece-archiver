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

## 2. Reference Indexing Subtask

Read `reference-indexing-workflow.md` before changing title, venue, year, DOI,
official link, publication status, `paper_reference/INDEX.md`, report references,
or baseline-facing citation metadata.

For each affected paper:

- collect local claims from PDFs, summaries, index files, report drafts, audit
  data, and category summaries
- verify formal publication metadata against official venue, journal,
  proceedings, anthology, publisher, DOI, or equivalent sources
- record an evidence table when the change affects a report, baseline decision,
  survey conclusion, or more than one local file
- use `待核查` when official evidence is not found after a bounded search

Do not infer that a paper is unpublished, non-main, or not accepted from a failed
search. That conclusion needs positive evidence.

## 3. Classification

Read `classification-rules.md` before assigning categories.

Decision order:

1. Prefer an existing category if the paper's main contribution clearly fits one.
2. Create a new category only when no existing category fits cleanly and the direction is likely to recur, or the user explicitly asks for a new category.
3. When in doubt between two categories, classify by the paper's main contribution, not by a secondary technique.

## 4. Parallel Writing

If there are at least 3 papers, split paper-level writing across subagents unless the user explicitly asks not to, or subagents are unavailable in the runtime environment.

Main agent keeps ownership of:

- category structure
- PDF moves
- `paper_reference/INDEX.md`
- category `研究方向总结.md`

Subagents only write:

- `<Title>.md`
- `<Title> - 中文翻译.md`

Each subagent assignment must require full-paper inspection, a detailed summary, and a full Chinese translation for every assigned paper. The assignment must state that a short abstract-level output is incomplete.

## 5. Per-Paper Files

For each paper, produce:

- summary file: `<English Title>.md`
- translation file: `<English Title> - 中文翻译.md`
- linked PDF in the same folder

Summary files must follow `paper_reference/论文阅读总结模板.md`.

The summary file is a detailed reading note. It must cover the paper's motivation, problem setting, method, assumptions, datasets or experimental setup, main results, limitations, and reusable technical details. Do not summarize only the abstract, introduction, and conclusion. Every substantive method, experiment, formula, algorithm, or central claim in the paper should be represented with paper-location citations when practical.

Translation files should preserve:

- section structure
- paragraph-level meaning of the main text
- formulas
- equation numbers
- algorithm blocks
- important tables and figures

Translation files must be full Chinese translations of the paper's main content, not section summaries. Translate body sections in paper order. If a very long appendix contains repetitive numeric tables with little explanatory content, it may be summarized briefly, but formulas, algorithm steps, methodological details, and critical experimental settings should still be preserved.

If text extraction quality makes full reading or full translation impossible, report the blocker and repair with rendered pages when practical. Do not silently shorten the output.

## 6. Formula and Table Recovery

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

## 7. Move PDFs

Only move PDFs after the paper-level files are done.

Keep the original PDF filename unless there is an explicit repo convention to rename it.

## 8. Update Shared Files

Update index with:

```bash
python scripts/update_paper_index.py --root .
```

Then manually update every touched category's `研究方向总结.md`.

If a new category is created, add its own `研究方向总结.md`.

## 9. Verify

Run:

```bash
python scripts/verify_paper_archive.py --root . --category "<touched-category>"
```

Before reporting completion, confirm:

- `paper_reference/temp` is empty or only contains files intentionally left for later
- no summary links still point to `../temp/`
- every new paper has summary, translation, and linked PDF
- `INDEX.md` count matches actual paper count
- title, venue, year, DOI, official link, and publication status follow
  `reference-indexing-workflow.md`

If the repository already contains older archive inconsistencies outside the current task, restrict verification to the categories you touched.
