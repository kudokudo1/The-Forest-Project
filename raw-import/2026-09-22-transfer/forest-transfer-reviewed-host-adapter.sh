#!/bin/bash

echo "FOREST — PHASE 14.10E.2A.5B.1"
echo "TRANSFER REVIEWED HOST ADAPTER"
echo "============================================================"

umask 077

TMP="$HOME/forest-qubes-i3-x11.REVIEW.py"

rm -f "$TMP"

/usr/bin/qvm-run \
  --pass-io \
  --no-shell \
  Cherry-AI \
  -- \
  cat \
  /home/user/The-Forest/bristlecone/ui/presentation_host_adapters/qubes_i3_x11.py \
  > "$TMP"

echo
echo "=== TRANSFER RESULT ==="
ls -l "$TMP"

echo
echo "=== SHA-256 ==="
sha256sum "$TMP"

echo
echo "=== PYTHON SYNTAX CHECK ==="
python3 -m py_compile "$TMP" \
&& echo "PASS: transferred adapter compiles"

echo
echo "=== BEGINNING OF FILE ==="
sed -n '1,55p' "$TMP"

echo
echo "============================================================"
echo "Adapter executed: NO"
echo "Installed permanently: NO"
echo "PHASE 14.10E.2A.5B.1: TRANSFERRED FOR REVIEW"
