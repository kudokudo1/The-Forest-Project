#!/bin/bash

echo "FOREST — PHASE 14.10E.2A.5B.2"
echo "VERIFY + INSTALL REVIEWED HOST ADAPTER"
echo "============================================================"

REVIEW="$HOME/forest-qubes-i3-x11.REVIEW.py"

SOURCE="/home/user/The-Forest/bristlecone/ui/presentation_host_adapters/qubes_i3_x11.py"

INSTALL_DIR="$HOME/.local/lib/the-forest/presentation_host_adapters"
INSTALL="$INSTALL_DIR/qubes_i3_x11.py"

echo
echo "=== HASH PARITY ==="

LOCAL_SHA="$(sha256sum "$REVIEW" | awk '{print $1}')"

REMOTE_SHA="$(
    /usr/bin/qvm-run \
        --pass-io \
        --no-shell \
        Cherry-AI \
        -- \
        sha256sum \
        "$SOURCE" |
    awk '{print $1}'
)"

echo "Cherry source : $REMOTE_SHA"
echo "dom0 review   : $LOCAL_SHA"

if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
    echo
    echo "FAIL: hashes differ — NOT INSTALLING"
    exit 1
fi

echo "PASS: reviewed copy exactly matches authoritative Forest source"

echo
echo "=== INSTALL USER-LOCAL TRUSTED COPY ==="

mkdir -p "$INSTALL_DIR"

if [ -e "$INSTALL" ]; then
    BACKUP="$INSTALL.backup.$(date -u +%Y%m%dT%H%M%SZ)"
    cp -p "$INSTALL" "$BACKUP"
    echo "Previous copy backed up:"
    echo "$BACKUP"
fi

cp "$REVIEW" "$INSTALL"
chmod 700 "$INSTALL"

echo "Installed:"
ls -l "$INSTALL"

echo
echo "=== INSTALLED HASH ==="

INSTALLED_SHA="$(sha256sum "$INSTALL" | awk '{print $1}')"

echo "$INSTALLED_SHA"

if [ "$INSTALLED_SHA" != "$LOCAL_SHA" ]; then
    echo "FAIL: installed copy hash mismatch"
    exit 1
fi

echo "PASS: installed copy exactly matches reviewed copy"

echo
echo "=== PYTHON SYNTAX ==="

python3 -m py_compile "$INSTALL" \
    && echo "PASS: installed adapter compiles"

echo
echo "=== PURE SELF-TEST ==="

python3 "$INSTALL" --self-test

echo
echo "=== HOST CAPABILITY PROBE ==="

python3 "$INSTALL" --probe

echo
echo "============================================================"
echo "Real Forest window manipulated: NO"
echo "Reasoning state modified: NO"
echo "i3 config modified: NO"
echo "picom config modified: NO"
echo
echo "PHASE 14.10E.2A.5B.2: INSTALLED + OFFLINE TESTED"
