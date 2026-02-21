#!/bin/bash
cd "$(dirname "$0")"

VENV_DIR="venv"
PYTHON_EXEC="$VENV_DIR/bin/python3"

if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Error: Virtual environment not found or Python executable is missing."
    echo "Please run the installation script first."
    exit 1
fi

echo "pasty"

$PYTHON_EXEC -u src/main.py "$@"