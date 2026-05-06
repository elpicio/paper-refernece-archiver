#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 <pdf> <page> [output-prefix]" >&2
  exit 1
fi

pdf_path="$1"
page="$2"
output_prefix="${3:-/tmp/paper-page}"
resolution="${PDF_RENDER_DPI:-220}"

if ! command -v pdftoppm >/dev/null 2>&1; then
  echo "missing required binary: pdftoppm" >&2
  exit 1
fi

pdftoppm -png -r "$resolution" -f "$page" -l "$page" "$pdf_path" "$output_prefix" >/dev/null 2>&1

printf "%s-%02d.png\n" "$output_prefix" "$page"
