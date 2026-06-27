# Reference Indexing Workflow

This workflow is required when adding papers to `paper_reference`, updating
`paper_reference/INDEX.md`, correcting title, venue, year, DOI, official link,
publication status, or using the archive as evidence for a report or baseline.

The goal is to make the archive usable as a citation source of truth. A failed
search is not evidence that a paper was not formally published.

## 1. Collect Local Claims

For each paper, collect the local claims before searching:

- PDF path and file name
- extracted title, authors, abstract, DOI, arXiv ID, OpenReview ID, or article ID
- title, venue, year, and status in existing summary files, `INDEX.md`, audit data,
  report drafts, or category summaries
- code, dataset, benchmark, or artifact links if they affect whether the paper can
  be used as a baseline

Treat local files and PDF metadata as clues only. They do not confirm formal
publication by themselves.

## 2. Use Source Priority

Use sources in this order:

1. Official venue, journal, proceedings, anthology, or publisher page. Examples:
   AAAI OJS, NeurIPS proceedings, ACL Anthology, PMLR, official ICLR OpenReview
   entries, ACM Digital Library, IEEE Xplore, Springer, Elsevier, Oxford, or a
   journal site.
2. DOI resolver, Crossref, DBLP, Semantic Scholar, or Google Scholar. These can
   help find the official page, but should not override it.
3. arXiv, local PDFs, project pages, GitHub repositories, and search snippets.
   These are useful clues, but they do not prove formal publication.

If an official source and a secondary source conflict, keep the official source
as the citation basis and record the conflict.

## 3. Archive Metadata Standard

For each indexed paper, keep these fields consistent across the summary file,
evidence table, report references, audit data, and generated index:

- official title
- authors
- year
- venue or journal
- publication status
- DOI, official URL, and preprint URL when available
- local PDF path, summary path, and translation path
- category
- artifact status, including code, data, benchmark, or reproduction package when
  it affects project use
- verification decision and evidence date

The generated `paper_reference/INDEX.md` remains a reading index. Do not overload
it with long metadata. Detailed citation evidence should live in the paper
summary, evidence table, audit data, or category-level verification record.

## 4. Search Ladder

Use deterministic searches before making any conclusion:

- exact title plus the likely official domain
- official proceedings index for the conference or journal issue
- DOI landing page if a DOI exists
- arXiv page fields such as DOI, journal reference, comments, and linked versions
- DBLP, Crossref, Semantic Scholar, or Google Scholar only to discover official
  links that were missed

Common official-domain searches:

- AAAI: `site:ojs.aaai.org/index.php/AAAI "<exact title>"`
- NeurIPS: `site:proceedings.neurips.cc "<exact title>"`
- ICML, AISTATS, COLT, UAI: `site:proceedings.mlr.press "<exact title>"`
- ICLR: `site:openreview.net/forum "<exact title>"`
- ACL, EMNLP, NAACL, COLING: `site:aclanthology.org "<exact title>"`
- ACM venues: `site:dl.acm.org "<exact title>"`
- IEEE venues: `site:ieeexplore.ieee.org "<exact title>"`

If the user provides an official-looking URL, open that URL first and verify that
the title, authors, venue, year, and article status match the local paper.

## 5. Decision Labels

Use one of these labels while deciding:

- `confirmed_official`: an official source confirms the title, authors, venue,
  year, and publication status.
- `confirmed_preprint`: only preprint or local evidence is available after the
  official-source search. This is not a claim that the paper was rejected or will
  never be published.
- `conflict_unresolved`: official and local records conflict, or two official
  records cannot be reconciled from available evidence.
- `not_found_official`: the bounded search did not find an official page. Keep
  affected metadata as `待核查` rather than converting it into a negative claim.

Never change a paper to non-main, unpublished, or not accepted only because the
first search did not find an official page.

## 6. Evidence Table

Before editing citation metadata, prepare an evidence table. For a small task it
can be included in the final response. For a batch task, or any correction that
affects a report, baseline choice, or survey conclusion, persist it as a local
record such as `paper_reference/参考文献核查记录.md` or a category-level
`参考文献核查记录.md`.

Use this schema:

| Item | Local claim | Official evidence | Secondary evidence | Decision | Action |
| --- | --- | --- | --- | --- | --- |
| Paper title | venue/year/status from local files | official URL, DOI, article ID | arXiv, DBLP, Crossref, etc. | decision label | files to update |

The evidence table must distinguish no official source found from official source
does not exist. The second statement requires strong evidence and should rarely
be used.

## 7. Update Rules

When a paper is confirmed:

- use the official title spelling in report references and formal metadata
- use the official venue, year, DOI, and official URL in summaries when available
- keep arXiv links as preprint links, not as substitutes for official links
- if the official title differs from the local filename, rename the summary and
  translation files only after checking that links and generated indexes can be
  updated consistently
- run the index-generation script instead of manually editing generated index
  structure

When a paper is unresolved:

- keep uncertain fields as `待核查`
- do not downgrade or promote the paper based on absence from search results
- record the exact search path or source gap in the evidence table
- tell the user which field remains unresolved

## 8. Verification

After edits, verify both file consistency and metadata consistency:

- regenerate `paper_reference/INDEX.md`
- run `verify_paper_archive.py` for touched categories
- search for old titles, old venue-year claims, stale arXiv-only claims, and stale
  PDF paths with `rg`
- confirm every corrected report reference uses the same official title, venue,
  year, DOI, and URL as the archive
- report unresolved items explicitly instead of presenting the archive as fully
  confirmed
