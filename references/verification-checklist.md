# Verification Checklist

Run the verification script:

```bash
python scripts/verify_paper_archive.py --root . --category "<touched-category>"
```

Then manually confirm:

- every newly archived paper has:
  English summary, Chinese translation, PDF
- summary file PDF links resolve inside the final category
- no summary still links to `../temp/`
- every touched category has `研究方向总结.md`
- `paper_reference/INDEX.md` count matches the actual number of indexed papers
- if formula extraction was damaged, the affected equations were repaired from rendered page images
- `paper_reference/temp` is empty unless the user explicitly left files for later

If there are known legacy issues elsewhere in `paper_reference`, verify only the categories touched by the current task.

Do not report completion as if the archive were done if any of these checks fail.
