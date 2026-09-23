#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${HOME}/The-Forest/bristlecone"
PID_FILE="${WORKSPACE}/logs/bristlecone-api.pid"

if [[ ! -f "${PID_FILE}" ]]; then
  echo "No Bristlecone API PID file was found."
  echo "Checking whether the port still responds..."
  if curl -fsS http://127.0.0.1:8643/health >/dev/null 2>&1; then
    echo "Port 8643 is active, but it was not started by this helper."
    echo "Use 'hermes -p bristlecone gateway stop' or inspect the running process."
    exit 1
  fi
  echo "Bristlecone API is already stopped."
  exit 0
fi

pid="$(cat "${PID_FILE}")"
if kill -0 "${pid}" 2>/dev/null; then
  kill "${pid}"
  for _ in $(seq 1 10); do
    if ! kill -0 "${pid}" 2>/dev/null; then
      break
    fi
    sleep 1
  done
fi

rm -f "${PID_FILE}"

if curl -fsS http://127.0.0.1:8643/health >/dev/null 2>&1; then
  echo "The API still responds. Another gateway process may be using port 8643."
  exit 1
fi

echo "Bristlecone API stopped. Newelle is disconnected from this local endpoint."
