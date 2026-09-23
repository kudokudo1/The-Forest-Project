#!/usr/bin/env bash
set -euo pipefail

PROFILE="bristlecone"
PROFILE_HOME="${HOME}/.hermes/profiles/${PROFILE}"
WORKSPACE="${HOME}/The-Forest/bristlecone"
BACKUPS="${HOME}/The-Forest/backups"
STAMP="$(date +%Y%m%d-%H%M%S)"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${PROFILE_HOME}/.env"
CONNECTION_FILE="${WORKSPACE}/NEWELLE-CONNECTION.txt"

echo "=== Planting Bristlecone Pine 0.0.2 ==="

command -v hermes >/dev/null 2>&1 || {
  echo "Hermes is not available in PATH."
  exit 1
}

mkdir -p "${BACKUPS}" "${WORKSPACE}"

if hermes profile show "${PROFILE}" >/dev/null 2>&1; then
  echo "Existing Bristlecone profile found."
  echo "Creating a safety export..."
  hermes profile export "${PROFILE}" \
    -o "${BACKUPS}/bristlecone-before-seed-0.0.2-${STAMP}.tar.gz"
else
  echo "Creating Bristlecone as a separate profile..."
  if hermes profile show default >/dev/null 2>&1; then
    hermes profile create "${PROFILE}" \
      --clone-from default \
      --description "Forest-aware multi-model Treewright for Tree, plugin, add-on, coding, testing, training-data, and standards development."
  else
    hermes profile create "${PROFILE}" \
      --description "Forest-aware multi-model Treewright for Tree, plugin, add-on, coding, testing, training-data, and standards development."
  fi
fi

mkdir -p "${PROFILE_HOME}" "${WORKSPACE}"

if [[ -f "${PROFILE_HOME}/SOUL.md" ]]; then
  cp -a "${PROFILE_HOME}/SOUL.md" \
    "${BACKUPS}/bristlecone-SOUL-before-seed-0.0.2-${STAMP}.md"
fi

if [[ -f "${WORKSPACE}/AGENTS.md" ]]; then
  cp -a "${WORKSPACE}/AGENTS.md" \
    "${BACKUPS}/bristlecone-AGENTS-before-seed-0.0.2-${STAMP}.md"
fi

cp "${SCRIPT_DIR}/SOUL.md" "${PROFILE_HOME}/SOUL.md"
cp -a "${SCRIPT_DIR}/workspace/." "${WORKSPACE}/"
cp "${SCRIPT_DIR}/seed-manifest.json" "${WORKSPACE}/seed-manifest.json"
cp "${SCRIPT_DIR}/FIRST-CONVERSATION.txt" "${WORKSPACE}/FIRST-CONVERSATION.txt"
cp "${SCRIPT_DIR}/NEWELLE-PROFILE-INSTRUCTIONS.txt" "${WORKSPACE}/NEWELLE-PROFILE-INSTRUCTIONS.txt"
cp "${SCRIPT_DIR}/docs/API-ARCHITECTURE.md" "${WORKSPACE}/API-ARCHITECTURE.md"

touch "${ENV_FILE}"
chmod 600 "${ENV_FILE}"

upsert_env() {
  local key="$1"
  local value="$2"
  local tmp
  tmp="$(mktemp)"
  awk -v key="${key}" -F= '$1 != key { print }' "${ENV_FILE}" > "${tmp}"
  printf '%s=%s\n' "${key}" "${value}" >> "${tmp}"
  mv "${tmp}" "${ENV_FILE}"
  chmod 600 "${ENV_FILE}"
}

existing_key="$(awk -F= '$1=="API_SERVER_KEY" {sub(/^[^=]*=/,""); print; exit}' "${ENV_FILE}" || true)"
if [[ -n "${existing_key}" ]]; then
  API_KEY="${existing_key}"
  echo "Keeping the existing Bristlecone API key."
else
  if command -v openssl >/dev/null 2>&1; then
    API_KEY="$(openssl rand -hex 32)"
  else
    API_KEY="$(python3 - <<'PY'
import secrets
print(secrets.token_hex(32))
PY
)"
  fi
  echo "Generated a new private Bristlecone API key."
fi

upsert_env "API_SERVER_ENABLED" "true"
upsert_env "API_SERVER_HOST" "127.0.0.1"
upsert_env "API_SERVER_PORT" "8643"
upsert_env "API_SERVER_MODEL_NAME" "bristlecone"
upsert_env "API_SERVER_KEY" "${API_KEY}"

# Explicitly remove permissive browser CORS from previous attempts.
tmp="$(mktemp)"
awk -F= '$1 != "API_SERVER_CORS_ORIGINS" { print }' "${ENV_FILE}" > "${tmp}"
mv "${tmp}" "${ENV_FILE}"
chmod 600 "${ENV_FILE}"

hermes -p "${PROFILE}" config set terminal.cwd "${WORKSPACE}"

cat > "${CONNECTION_FILE}" <<EOF
BRISTLECONE PINE — NEWELLE CONNECTION

Provider: OpenAI API
API Endpoint: http://127.0.0.1:8643/v1/
Canonical Base URL: http://127.0.0.1:8643/v1
OpenAI Model: bristlecone
API Key: ${API_KEY}

This file contains a private local API key.
Do not publish or commit it.
EOF
chmod 600 "${CONNECTION_FILE}"

# Replace placeholders in helper scripts with no secrets embedded.
chmod +x "${WORKSPACE}/bin/"*.sh

echo
echo "Bristlecone Pine Seed 0.0.2 has been planted."
echo "Profile:   ${PROFILE_HOME}"
echo "Workspace: ${WORKSPACE}"
echo "API:       http://127.0.0.1:8643/v1"
echo
echo "Start the API with:"
echo "  ${WORKSPACE}/bin/start-bristlecone-api.sh"
echo
echo "Show Newelle connection values with:"
echo "  ${WORKSPACE}/bin/show-newelle-connection.sh"
echo
echo "The model/provider settings were cloned from the default profile when available."
echo "Verify them with: bristlecone model"
