#!/usr/bin/env bash
set -euo pipefail

PROFILE_ENV="${HOME}/.hermes/profiles/bristlecone/.env"
BASE="http://127.0.0.1:8643"

if [[ ! -f "${PROFILE_ENV}" ]]; then
  echo "Bristlecone profile environment was not found."
  exit 1
fi

KEY="$(awk -F= '$1=="API_SERVER_KEY" {sub(/^[^=]*=/,""); print; exit}' "${PROFILE_ENV}")"
if [[ -z "${KEY}" ]]; then
  echo "API_SERVER_KEY is missing."
  exit 1
fi

echo "=== Health ==="
curl -fsS "${BASE}/health"
echo

echo "=== Models ==="
curl -fsS \
  -H "Authorization: Bearer ${KEY}" \
  "${BASE}/v1/models"
echo

echo "=== Chat Test ==="
curl -fsS \
  -H "Authorization: Bearer ${KEY}" \
  -H "Content-Type: application/json" \
  "${BASE}/v1/chat/completions" \
  -d '{
    "model": "bristlecone",
    "messages": [
      {
        "role": "user",
        "content": "Reply with your name, role, and the meaning of Pine is fine. Do not use tools."
      }
    ],
    "stream": false
  }'
echo
