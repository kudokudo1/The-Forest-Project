#!/bin/bash

echo "FOREST — PHASE 14.10E.2A.3"
echo "PRESENTATION ADAPTER DISCOVERY"
echo "============================================================"
echo

echo "=== CLICK THE FOREST REASONING WINDOW ==="
xprop \
  WM_CLASS \
  WM_NAME \
  _NET_WM_NAME \
  _NET_WM_WINDOW_TYPE \
  _NET_WM_PID \
  _QUBES_VMNAME

echo
echo "=== WINDOW MANAGER ==="
i3-msg -t get_version 2>/dev/null || echo "i3-msg unavailable"
pgrep -a i3 2>/dev/null || echo "No i3 process reported"

echo
echo "=== DESKTOP / SESSION ==="
printf 'XDG_SESSION_TYPE=%s\n' "${XDG_SESSION_TYPE:-unset}"
printf 'XDG_CURRENT_DESKTOP=%s\n' "${XDG_CURRENT_DESKTOP:-unset}"
printf 'DESKTOP_SESSION=%s\n' "${DESKTOP_SESSION:-unset}"
printf 'DISPLAY=%s\n' "${DISPLAY:-unset}"

echo
echo "=== MONITORS ==="
xrandr --listmonitors 2>/dev/null || echo "xrandr monitor information unavailable"

echo
echo "=== COMPOSITOR ==="
pgrep -a picom 2>/dev/null \
  || pgrep -a compton 2>/dev/null \
  || echo "No picom/compton process reported"

echo
echo "=== LIKELY I3 / COMPOSITOR CONFIG FILES ==="
find "$HOME/.config" \
  -maxdepth 4 \
  -type f \
  \( \
    -path '*/i3/*' \
    -o -iname '*picom*' \
    -o -iname '*compton*' \
  \) \
  -print 2>/dev/null

echo
echo "============================================================"
echo "Files modified: NONE"
echo "PHASE 14.10E.2A.3 DISCOVERY: CAPTURED"
