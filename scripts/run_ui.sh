#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' "${ROOT_DIR}/.env" | xargs)
fi

export PYTHONPATH="${ROOT_DIR}:${PYTHONPATH:-}"
PORT="${AFI_PORT:-8507}"

if command -v streamlit >/dev/null 2>&1; then
  exec streamlit run "${ROOT_DIR}/app.py" --server.port "${PORT}" --server.headless true
fi

echo "Streamlit nao encontrado. Executando UI fallback."
exec python "${ROOT_DIR}/ui_fallback/ui_fallback_server.py" --port "${PORT}"
