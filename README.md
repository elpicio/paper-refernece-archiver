# Paper Reference Archiver

Codex skill for maintaining a `paper_reference` archive: scan new PDFs, classify papers, write summaries and Chinese translations, repair damaged formulas from rendered PDF pages, regenerate the paper index, and verify archive consistency.

## Contents

- `SKILL.md`: skill entry point and operating rules
- `references/`: workflow, classification, writing, and verification guidance
- `scripts/`: helper scripts for scanning PDFs, extracting signals, updating the index, rendering pages, and verifying the archive
- `agents/`: optional agent metadata

## Expected Repository Layout

The target research repository should contain:

```text
paper_reference/
  INDEX.md
  temp/
  论文阅读总结模板.md
  <category>/
    研究方向总结.md
```

New PDFs are expected in `paper_reference/temp`. Archived papers are placed under category directories.

## Requirements

- Python 3.10+
- Poppler command-line tools:
  - `pdfinfo`
  - `pdftotext`
  - `pdftoppm`

On Ubuntu or Debian:

```bash
sudo apt-get install poppler-utils
```

## Script Usage

Run commands from this skill checkout, and pass the target research repository through `--root`:

```bash
python scripts/scan_temp_papers.py --root /path/to/research-repo
python scripts/extract_pdf_signals.py --root /path/to/research-repo --pdf paper_reference/temp/example.pdf
python scripts/update_paper_index.py --root /path/to/research-repo
python scripts/verify_paper_archive.py --root /path/to/research-repo --category "long-form calibration"
bash scripts/render_pdf_page.sh /path/to/research-repo/paper_reference/<category>/<file>.pdf 5
```

If the skill is installed under another directory, call the scripts through that installed path and keep `--root` pointed at the repository being archived.

## License

MIT
