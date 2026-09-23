#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${HOME}/The-Forest/bristlecone"
PID_FILE="${WORKSPACE}/logs/bristlecone-api.pid"

echo "=== Bristlecone API Status ==="

if curl -fsS http://127.0.0.1:8643/health; then
  echo
  echo "Endpoint: http://127.0.0.1:8643/v1"
  echo "Status: running"
else
  echo "Status: not responding"
fi

if [[ -f "${PID_FILE}" ]]; then
  echo "Recorded PID: $(cat "${PID_FILE}")"
else
  echo "Recorded PID: none"
fi
