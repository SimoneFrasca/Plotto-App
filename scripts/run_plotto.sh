#!/bin/bash

# Ottieni la cartella "script" dove si trova questo file
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Esempio di lancio di un file Python (modifica con il tuo comando reale)
python3 "$BASE_DIR/src/app.py"
# oppure, se è eseguibile direttamente