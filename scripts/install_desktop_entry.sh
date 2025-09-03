#!/bin/bash
set -e

APP_NAME="plotto"
DESKTOP_FILE="$PWD/desktop/plotto.desktop"
TARGET_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

echo "Installing desktop entry to $TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp "$DESKTOP_FILE" "$TARGET_DIR/$APP_NAME.desktop"

# Copia anche sulla Scrivania (se esiste)
if [ -d "$HOME/Scrivania" ]; then
    cp "$DESKTOP_FILE" "$HOME/Scrivania/$APP_NAME.desktop"
    chmod +x "$HOME/Scrivania/$APP_NAME.desktop"
fi

update-desktop-database "$TARGET_DIR" || true

echo "✅ Installazione completata!"
