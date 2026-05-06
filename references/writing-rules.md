# Writing Rules

## Summary Files

Use `paper_reference/论文阅读总结模板.md` exactly as the structural template.

Requirements:

- default to Chinese
- first mention of an English term should be `English term（中文解释）`
- distinguish author claims from your own judgment
- if information is not confirmed from the paper, write `未确认`
- cite locations such as `Abstract`, `Sec. 3`, `Table 2`, `Fig. 4` when practical
- optimize for information density, not praise or filler

## Translation Files

Translation file name:

- `<English Title> - 中文翻译.md`

Requirements:

- preserve section hierarchy
- preserve formulas and equation numbers
- preserve algorithms and important tables
- keep terminology stable across the file
- when `pdftotext` damages formulas or tables, repair them via rendered page images and vision before finishing

If an appendix contains long repetitive tables with little explanatory content, it may be compressed, but do not compress away formulas, algorithm steps, or critical experimental settings.

## Summary File Links

Inside the English summary file, the PDF link should normally be:

```md
**链接**：[PDF](./<pdf-filename>.pdf)
```

Do not leave links pointing to `../temp/`.

## Category Research Summaries

Every touched category should have or update `研究方向总结.md`.

That file should answer four things:

1. what papers in this category share
2. how the line evolved over time
3. what is still unresolved
4. what datasets or evaluation settings are common

When a new category is created, write its `研究方向总结.md` during the same task.

## What Not to Do

- do not fabricate titles, authors, datasets, or equations
- do not hide extraction failures
- do not stop after writing paper-level files if the user asked for the full archive flow
- do not update `INDEX.md` manually when the script can regenerate it
