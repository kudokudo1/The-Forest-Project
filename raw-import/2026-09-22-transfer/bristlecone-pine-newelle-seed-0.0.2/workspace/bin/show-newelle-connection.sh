#!/usr/bin/env bash
set -euo pipefail

FILE="${HOME}/The-Forest/bristlecone/NEWELLE-CONNECTION.txt"

if [[ ! -f "${FILE}" ]]; then
  echo "Connection file not found. Run the planting script first."
  exit 1
fi

cat "${FILE}"
