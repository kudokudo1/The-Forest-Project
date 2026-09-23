#!/usr/bin/env bash
set -euo pipefail

PROFILE_HOME="${HOME}/.hermes/profiles/bristlecone"
WORKSPACE="${HOME}/The-Forest/bristlecone"

echo "=== PROFILE ==="
hermes profile show bristlecone

echo
echo "=== REQUIRED FILES ==="
for item in \
  "${PROFILE_HOME}/SOUL.md" \
  "${PROFILE_HOME}/.env" \
  "${WORKSPACE}/AGENTS.md" \
  "${WORKSPACE}/seed-manifest.json" \
  "${WORKSPACE}/FIRST-CONVERSATION.txt" \
  "${WORKSPACE}/NEWELLE-CONNECTION.txt" \
  "${WORKSPACE}/NEWELLE-PROFILE-INSTRUCTIONS.txt" \
  "${WORKSPACE}/corpus" \
  "${WORKSPACE}/proposals" \
  "${WORKSPACE}/evaluations" \
  "${WORKSPACE}/receipts" \
  "${WORKSPACE}/learning/candidates" \
  "${WORKSPACE}/learning/approved"
do
  if [[ -e "${item}" ]]; then
    echo "OK   ${item}"
  else
    echo "MISS ${item}"
  fi
done

echo
echo "=== API SETTINGS ==="
awk -F= '
  $1=="API_SERVER_ENABLED" ||
  $1=="API_SERVER_HOST" ||
  $1=="API_SERVER_PORT" ||
  $1=="API_SERVER_MODEL_NAME" {
    print
  }
  $1=="API_SERVER_KEY" {
    print "API_SERVER_KEY=[configured and hidden]"
  }
' "${PROFILE_HOME}/.env"

echo
echo "=== OLLAMA MODELS ==="
ollama list 2>/dev/null || true

echo
echo "Verification finished. This script does not change the profile."
