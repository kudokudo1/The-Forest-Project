#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${HOME}/The-Forest/bristlecone"
PID_FILE="${WORKSPACE}/logs/bristlecone-api.pid"
LOG_FILE="${WORKSPACE}/logs/bristlecone-api.log"
URL="http://127.0.0.1:8643/health"

mkdir -p "${WORKSPACE}/logs"

if curl -fsS "${URL}" >/dev/null 2>&1; then
  echo "Bristlecone API is already running at http://127.0.0.1:8643/v1"
  exit 0
fi

if [[ -f "${PID_FILE}" ]]; then
  old_pid="$(cat "${PID_FILE}" || true)"
  if [[ -n "${old_pid}" ]] && kill -0 "${old_pid}" 2>/dev/null; then
    echo "A Bristlecone gateway process is already running with PID ${old_pid}."
    exit 0
  fi
  rm -f "${PID_FILE}"
fi

echo "Starting Bristlecone's Hermes gateway..."
nohup hermes -p bristlecone gateway run >> "${LOG_FILE}" 2>&1 &
pid="$!"
echo "${pid}" > "${PID_FILE}"

for _ in $(seq 1 20); do
  if curl -fsS "${URL}" >/dev/null 2>&1; then
    echo "Bristlecone API is ready at http://127.0.0.1:8643/v1"
    echo "PID: ${pid}"
    exit 0
  fi
  if ! kill -0 "${pid}" 2>/dev/null; then
    echo "The gateway exited before becoming ready."
    echo "Recent log output:"
    tail -n 40 "${LOG_FILE}" || true
    exit 1
  fi
  sleep 1
done

echo "The process is running but the API did not become ready within 20 seconds."
echo "Check: ${LOG_FILE}"
exit 1
