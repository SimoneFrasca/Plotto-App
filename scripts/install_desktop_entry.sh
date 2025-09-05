#!/bin/bash
set -e

APP_NAME="plotto"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # path assoluto della cartella Plotto-App
DESKTOP_FILE="$BASE_DIR/desktop/plotto.desktop"
TARGET_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

echo "Installing desktop entry to $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# Sostituisce __BASE_DIR__ con il percorso reale e installa
sed "s|__BASE_DIR__|$BASE_DIR|g" "$DESKTOP_FILE" > "$TARGET_DIR/$APP_NAME.desktop"

# Copia anche sulla Scrivania (se esiste)
if [ -d "$HOME/Scrivania" ]; then
    sed "s|__BASE_DIR__|$BASE_DIR|g" "$DESKTOP_FILE" > "$HOME/Scrivania/$APP_NAME.desktop"
    chmod +x "$HOME/Scrivania/$APP_NAME.desktop"
fi

update-desktop-database "$TARGET_DIR" || true

echo "✅ Installazione completata!"

