---
name: paper-reference-archiver
description: >-
  Use when the user wants to process new PDFs in `paper_reference/temp`:
  inspect and classify papers into existing or new categories, write paper
  summaries from the repository template, produce Chinese full translations,
  repair formulas or tables via PDF page rendering plus vision when text
  extraction is damaged, move PDFs into target folders, update
  `paper_reference/INDEX.md`, and refresh category `研究方向总结.md`.
---

# Paper Reference Archiver

Use this skill for a repository that maintains papers under `paper_reference`.
Script paths below are relative to this skill directory; resolve them before running commands from a target repository.

Read [references/workflow.md](references/workflow.md) at the start of the task.

Read other references only when needed:

- Read [references/classification-rules.md](references/classification-rules.md) when deciding whether a paper belongs to an existing category or requires a new one.
- Read [references/writing-rules.md](references/writing-rules.md) before writing summaries, translations, or `研究方向总结.md`.
- Read [references/verification-checklist.md](references/verification-checklist.md) before reporting completion.

## Core Workflow

1. Inventory new PDFs with:
   `python scripts/scan_temp_papers.py --root .`
2. For any ambiguous paper, inspect it more closely with:
   `python scripts/extract_pdf_signals.py --root . --pdf <relative-pdf-path>`
3. Decide the target category. Prefer an existing category unless the paper batch clearly defines a new direction.
4. Write per-paper files:
   summary `.md` from `paper_reference/论文阅读总结模板.md`
   translation ` - 中文翻译.md`
5. Only after per-paper files are ready, move each PDF into its final category directory.
6. Update `paper_reference/INDEX.md` with:
   `python scripts/update_paper_index.py --root .`
7. Update each touched category's `研究方向总结.md`.
8. Run:
   `python scripts/verify_paper_archive.py --root . --category "<touched-category>"`

## Ownership Rules

When multiple papers are being processed, use subagents if that materially speeds up the task.

- Main agent owns:
  category decisions, directory creation, PDF moves, `paper_reference/INDEX.md`, and all `研究方向总结.md`
- Subagents own:
  paper-level summary and translation files only

Do not let multiple agents write the same category summary or index file.

## Formula Repair Rule

If `pdftotext` damages a formula, denominator, superscript, subscript, table column, or algorithm layout:

1. Locate the relevant page from extracted text.
2. Render the page with:
   `bash scripts/render_pdf_page.sh <pdf> <page>`
3. Use visual inspection on the rendered image to recover the expression.
4. Patch the translation or notes file with the recovered formula.
5. Remove any temporary disclaimer that said the formula could not be reconstructed.

Do not leave obviously damaged formulas unresolved when the user asked for a full archive pass.

## Constraints

- Do not move PDFs before the summary and translation files exist.
- Do not touch unrelated changes elsewhere in the repo.
- Keep file names aligned with existing `paper_reference` conventions.
- Keep links inside paper summaries relative to the target directory, normally `./<pdf-name>.pdf`.
- Exclude `paper_reference/temp` and `paper_reference/datasets` from the generated paper index.
