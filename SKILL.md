---
name: paper-reference-archiver
description: >-
  Use when the user wants to process new PDFs in `paper_reference/temp`:
  inspect and classify papers into existing or new categories, write paper
  summaries from the repository template, produce Chinese full translations,
  repair formulas or tables via PDF page rendering plus vision when text
  extraction is damaged, move PDFs into target folders, update
  `paper_reference/INDEX.md`, verify citation metadata against official sources,
  correct title, venue, year, DOI, official link, publication status, and refresh
  category `研究方向总结.md`.
---

# Paper Reference Archiver

Use this skill for a repository that maintains papers under `paper_reference`.
Script paths below are relative to this skill directory; resolve them before running commands from a target repository.

Read [references/workflow.md](references/workflow.md) at the start of the task.

Read other references only when needed:

- Read [references/classification-rules.md](references/classification-rules.md) when deciding whether a paper belongs to an existing category or requires a new one.
- Read [references/reference-indexing-workflow.md](references/reference-indexing-workflow.md) before updating `paper_reference/INDEX.md`, correcting title, venue, year, DOI, official link, publication status, or using the archive as citation evidence.
- Read [references/writing-rules.md](references/writing-rules.md) before writing summaries, translations, or `研究方向总结.md`.
- Read [references/verification-checklist.md](references/verification-checklist.md) before reporting completion.

## Core Workflow

1. Inventory new PDFs with:
   `python scripts/scan_temp_papers.py --root .`
2. For any ambiguous paper, inspect it more closely with:
   `python scripts/extract_pdf_signals.py --root . --pdf <relative-pdf-path>`
3. Run the reference indexing subtask for title, venue, year, DOI, official link, publication status, and any report-facing citation metadata.
4. Decide the target category. Prefer an existing category unless the paper batch clearly defines a new direction.
5. Write per-paper files:
   summary `.md` from `paper_reference/论文阅读总结模板.md`
   translation ` - 中文翻译.md`
6. Only after per-paper files are ready, move each PDF into its final category directory.
7. Update `paper_reference/INDEX.md` with:
   `python scripts/update_paper_index.py --root .`
8. Update each touched category's `研究方向总结.md`.
9. Run:
   `python scripts/verify_paper_archive.py --root . --category "<touched-category>"`

## Reference Indexing Rule

Do not treat a failed search as evidence that a paper is unpublished, non-main,
or not formally accepted. Formal publication metadata must be based on official
venue, journal, proceedings, anthology, publisher, DOI, or equivalent sources.
When official evidence is not found after a bounded search, keep the field as
`待核查` and record the evidence gap.

## Mandatory Reading and Writing Standard

For every paper, the paper-level writer must inspect the full paper before writing. Do not rely only on the abstract, introduction, conclusion, metadata, or first-page excerpt.

Each summary must be a detailed reading note, not a short abstract. It must follow `paper_reference/论文阅读总结模板.md` and cover the paper's motivation, problem setting, method, assumptions, datasets or experimental setup, main results, limitations, and reusable technical details. If a section contains substantive methods, experiments, formulas, algorithms, or claims, represent it in the summary with paper-location citations when practical.

Each translation file must be a full Chinese translation of the paper's main content. Preserve the paper's section order, paragraph-level meaning, formulas, equation numbers, algorithm blocks, and important tables or figures. Do not replace body sections with brief summaries. Only repetitive appendix tables with little explanatory content may be compressed, and formulas, algorithm steps, and critical experimental settings must still be preserved.

Summaries and translations must follow the language style and terminology rules in `references/writing-rules.md`: use natural Chinese research writing, avoid machine-translation-like phrasing, keep established technical terms in their conventional form, and reject commercial jargon or unsupported promotional language.

If extraction quality prevents full reading or full translation, stop and report the blocker. Do not silently shorten the output.

## Ownership Rules

When at least three papers are being processed, use subagents for paper-level writing unless the user explicitly asks not to, or the runtime environment makes subagents unavailable.

- Main agent owns:
  category decisions, directory creation, PDF moves, `paper_reference/INDEX.md`, and all `研究方向总结.md`
- Subagents own:
  paper-level summary and translation files only

Every subagent assignment must explicitly include the mandatory reading and writing standard above, the repository summary template requirement, the language style and terminology rules, and the requirement to produce both the detailed summary and full Chinese translation for each assigned paper. The main agent must reject or revise subagent outputs that read like machine translation, force unnatural terminology translations, or contain commercial jargon or promotional phrasing.

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
