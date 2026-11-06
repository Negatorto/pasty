#!/bin/bash
cd "$(dirname "$0")"

VENV_DIR="venv"
PYTHON_EXEC="$VENV_DIR/bin/python3"

if [ ! -f "$PYTHON_EXEC" ]; then
    PYTHON_EXEC="python3"
fi

# Use X11 backend (XWayland) on GNOME Wayland so GTK4 can monitor and own
# the clipboard in the background even when the window is hidden/unfocused.
export GDK_BACKEND=x11

exec "$PYTHON_EXEC" -u src/main.py "$@"