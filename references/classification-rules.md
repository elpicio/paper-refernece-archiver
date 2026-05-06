# Classification Rules

Classify by the paper's main contribution, not by a minor component.

Prefer an existing category over a new category.

## Existing Categories

### atomic factuality

Use for papers whose main object is factuality assessment, claim verification, atomic fact scoring, or long-form factual precision.

### SE

Use for semantic entropy and related semantic-space uncertainty methods.

### benchmark

Use for general LLM UQ benchmarks, especially short-form, MCQ, clinical, or broad method comparison benchmarks.

### long-form calibration

Use for long-form generation calibration, confidence correction, or calibration-aware factuality improvement.

### long-form fine-grained UQ

Use for token-, sentence-, span-, claim-, or question-level long-form UQ when graph structure is not the main contribution.

### long-form graph UQ

Use for long-form UQ methods whose main object is a claim graph, entailment graph, paragraph graph, or structural graph used directly for uncertainty estimation.

### long-form benchmark

Use for long-form QA or long-form generation uncertainty benchmarks.

### reasoning topology

Use when the paper's main contribution is uncertainty, hallucination detection, risk control, or calibration over reasoning processes, reasoning-answer coupling, or agent trajectories.

This category includes papers without explicit graphs if the main target is still reasoning uncertainty or reasoning-answer validity.

Examples:

- `Understanding the Uncertainty of LLM Explanations`
- `Uncertainty Propagation on LLM Agent`
- `Joint Evaluation of Answer and Reasoning Consistency for Hallucination Detection in Large Reasoning Models`
- `Quantifying and Understanding Uncertainty in Large Reasoning Models`

### reasoning graph analysis

Use when the paper's main contribution is graph construction, graph probing, graph verification, or graph intervention over reasoning traces, but not itself a UQ method.

Examples:

- `Mapping the Minds of LLMs`
- `KisMATH`
- `Theorem-of-Thought`
- `Verifying Chain-of-Thought Reasoning via Its Computational Graph`

### sample-efficient

Use for single-sequence, low-sample, or sample-efficiency focused UQ methods.

### survey

Use for surveys, position pieces, and broad reviews of UQ.

### uncertainty expression

Use for natural language confidence expression, refusal calibration, or truth-aligned confidence verbalization.

## Boundary Cases

### reasoning topology vs reasoning graph analysis

Use `reasoning topology` if the paper is fundamentally about uncertainty or hallucination detection over reasoning, even if it uses reasoning-answer consistency rather than an explicit graph.

Use `reasoning graph analysis` if the paper is fundamentally about extracting or analyzing reasoning graphs, causal graphs, or computational graphs, but stops short of answer-level uncertainty quantification.

### reasoning topology vs long-form graph UQ

Use `long-form graph UQ` when the object is long-form response uncertainty and the graph is built over claims, paragraphs, entailment, or structure in generated responses.

Use `reasoning topology` when the object is reasoning traces, reasoning-answer support, or agent trajectories rather than long-form response graphs.

## When to Create a New Category

Create a new category only if all three conditions hold:

1. No existing category fits without distortion.
2. The direction is likely to recur.
3. The new category can be named by a clear research object, not by a one-off paper title.

If only one paper is unusual, usually keep it in the closest existing category and explain the mismatch in `研究方向总结.md`.

## Index Scope

`paper_reference/INDEX.md` should include category directories that contain English paper summary files.

Do not index:

- `paper_reference/temp`
- `paper_reference/datasets`
- `paper_reference/论文阅读总结模板.md`
