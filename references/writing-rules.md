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
- write a detailed reading note, not a short abstract or executive summary
- cover motivation, problem setting, method, assumptions, datasets or experimental setup, main results, limitations, and reusable technical details
- represent every substantive method, experiment, formula, algorithm, or central claim with enough detail that the reader can recover the paper's technical contribution without reopening the PDF

## Translation Files

Translation file name:

- `<English Title> - 中文翻译.md`

Requirements:

- provide a full Chinese translation of the paper's main content
- preserve section hierarchy
- preserve paragraph-level meaning in paper order
- preserve formulas and equation numbers
- preserve algorithms and important tables
- keep terminology stable across the file
- when `pdftotext` damages formulas or tables, repair them via rendered page images and vision before finishing

Do not replace body sections with brief summaries. If an appendix contains long repetitive tables with little explanatory content, it may be compressed, but do not compress away formulas, algorithm steps, methodological details, or critical experimental settings.

If full translation cannot be completed because extraction is damaged or pages are unreadable, report the blocker explicitly. Do not finish with a shortened translation while presenting it as complete.

## Language Style and Terminology

Summaries and translations must use natural written Chinese that follows Chinese language habits. The output should read like a Chinese researcher's reading note or technical translation, not like machine-translated English.

Use Chinese sentence structure by default. When an English sentence is long, split it into clear Chinese clauses when needed, while preserving the original meaning, logical relations, and technical claims. Do not mechanically preserve English word order, passive constructions, nominalized expressions, or source-language punctuation habits.

Do not produce machine-translation-like text. Avoid literal renderings that are grammatical but unnatural in Chinese, such as stacked `的` phrases, unnecessary `被` constructions, repeated use of `因此`, `此外`, or `值得注意的是`, and direct copying of English connective patterns.

Technical terms should follow established usage in the research community. Do not invent Chinese translations for terms that are conventionally used in English or mixed Chinese-English form. Terms such as `benchmark`, `token`, `prompt`, `embedding`, `attention`, `transformer`, `dataset`, `baseline`, `agent`, `rollout`, `ablation`, `fine-tuning`, `pretraining`, `retrieval`, `reranking`, `in-context learning`, `chain-of-thought`, and `reinforcement learning` may stay in English or use the common Chinese form when that form is already standard.

For first mention of a specialized term, use the most readable form. If the English term is the standard form, keep the English term and briefly explain it in Chinese. If a Chinese term is already standard, use the Chinese term and optionally include the English term in parentheses. After first mention, keep the same term form throughout the file.

Do not mechanically write every English term as `English term（中文解释）`. Use this form only when it helps comprehension or disambiguation.

Keep names, datasets, benchmarks, model names, method names, metrics, and system names in their original form unless the paper itself gives an official Chinese name. Do not translate proper nouns, acronym expansions, or benchmark names just to make the paragraph look fully Chinese.

Use precise academic wording. Prefer factual verbs such as `提出`, `定义`, `构造`, `估计`, `验证`, `比较`, `报告`, `显示`, `降低`, `提高`, `依赖`, `假设`, and `限制`. Avoid vague or promotional verbs such as `赋能`, `打造`, `驱动`, `革新`, `颠覆`, `释放潜力`, and `智能化升级` unless the source paper itself uses those expressions and the wording is analytically relevant.

Do not add commercial jargon, marketing tone, or inflated value judgments. Avoid phrases such as `业界领先`, `极致体验`, `革命性突破`, `全方位赋能`, `闭环能力`, `商业化落地`, `打造生态`, and `显著释放价值`. If the paper makes a strong claim, attribute it to the authors and keep the wording technical.

Do not rewrite papers into product copy. A method is not a `solution` unless the paper frames it that way. A framework is not a `platform` unless the paper says it is. A result should be described by the measured metric, dataset, and comparison target, not by unsupported praise.

Maintain an academic but readable tone. The writing should be clear, compact, and technically specific. Avoid overly formal translationese, casual internet language, rhetorical flourish, metaphor, motivational phrasing, and filler.

When translating, preserve meaning rather than word count. It is acceptable to split, merge, or reorder clauses inside a paragraph when this improves Chinese readability and does not change the claim, condition, contrast, or citation relation.

When summarizing, use Chinese research-note style. Prefer direct statements about what the paper does, how it does it, what evidence it gives, and what remains limited. Do not write generic praise or generic importance statements that could apply to any paper.

Before finishing each summary or translation, perform a language-quality pass. Check for unnatural literal translation, forced terminology translation, inconsistent terms, unsupported promotional language, repeated connective phrases, and sentences that a Chinese technical reader would find awkward.

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
- do not produce abstract-only or conclusion-only summaries
- do not replace full-paper translation with section summaries
- do not produce machine-translation-like Chinese
- do not force established technical terms into invented Chinese translations
- do not add commercial jargon, marketing tone, or unsupported praise
- do not stop after writing paper-level files if the user asked for the full archive flow
- do not update `INDEX.md` manually when the script can regenerate it
