#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
MYSTRAN_BIN=${MYSTRAN:-mystran}
mkdir -p "$ROOT/runs"
fail=0
pass=0
for deck in "$ROOT/eingabe"/*; do
  stem=$(basename "$deck")
  stem=${stem%.*}
  echo "=== $stem ==="
  if ! (cd "$ROOT/runs" && "$MYSTRAN_BIN" "$deck"); then
    echo "MYSTRAN failed for $stem"
    fail=$((fail+1))
    continue
  fi
  out=$(ls "$ROOT/runs/${stem}".F06 "$ROOT/runs/${stem}".f06 2>/dev/null | head -1 || true)
  if [[ -z "${out}" ]]; then
    echo "no F06 produced for $stem"
    fail=$((fail+1))
    continue
  fi
  if python3 "$ROOT/run_validation.py" --f06 "$out" --expected-json "$ROOT/referenz_werte.json" --case "$stem"; then
    pass=$((pass+1))
  else
    fail=$((fail+1))
  fi
done
echo "===================="
echo "$pass passed, $fail failed"
[[ $fail -eq 0 ]]
