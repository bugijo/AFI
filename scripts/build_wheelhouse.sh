#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WHEELHOUSE_DIR="${ROOT_DIR}/wheelhouse"

mkdir -p "${WHEELHOUSE_DIR}"

pip download --dest "${WHEELHOUSE_DIR}" --requirement "${ROOT_DIR}/requirements.txt"

cd "${WHEELHOUSE_DIR}"
zip -r "${ROOT_DIR}/wheels.zip" ./*
