#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "RouterGen development bootstrap"
echo "==============================="
echo "Project root : ${PROJECT_ROOT}"
echo "Python       : ${PYTHON_BIN}"
echo

if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
    echo "ERROR: ${PYTHON_BIN} was not found in PATH." >&2
    exit 1
fi

echo "[1/5] Checking Python version..."

"${PYTHON_BIN}" - <<'PY'
import sys

minimum = (3, 10)

if sys.version_info < minimum:
    print(
        f"ERROR: RouterGen requires Python "
        f"{minimum[0]}.{minimum[1]} or newer.",
        file=sys.stderr,
    )
    raise SystemExit(1)

print(
    "PASS: Python "
    f"{sys.version_info.major}."
    f"{sys.version_info.minor}."
    f"{sys.version_info.micro}"
)
PY

if [[ ! -d "${VENV_DIR}" ]]; then
    echo
    echo "[2/5] Creating virtual environment..."
    "${PYTHON_BIN}" -m venv "${VENV_DIR}"
else
    echo
    echo "[2/5] Virtual environment already exists."
fi

VENV_PYTHON="${VENV_DIR}/bin/python"
VENV_ROUTERGEN="${VENV_DIR}/bin/routergen"

if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "ERROR: Virtual environment Python is unavailable." >&2
    exit 1
fi

echo
echo "[3/5] Installing RouterGen development package..."

"${VENV_PYTHON}" -m pip install -e "${PROJECT_ROOT}[dev]"

echo
echo "[4/5] Running tests..."

(
    cd "${PROJECT_ROOT}"
    "${VENV_PYTHON}" -m pytest
)

echo
echo "[5/5] Running read-only environment diagnostics..."

"${VENV_ROUTERGEN}" diagnose

echo
echo "RouterGen development bootstrap completed successfully."
echo
echo "Activate with:"
echo "  source ${VENV_DIR}/bin/activate"
