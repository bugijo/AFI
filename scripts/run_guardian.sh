#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  # shellcheck disable=SC2046
  export $(grep -v '^#' "${ROOT_DIR}/.env" | xargs)
fi

export PYTHONPATH="${ROOT_DIR}:${PYTHONPATH:-}"
exec python "${ROOT_DIR}/guardiao.py"
