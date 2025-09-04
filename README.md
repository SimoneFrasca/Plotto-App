# Plotto App

Plotto è un'applicazione desktop per visualizzare e analizzare dati da file CSV e XML. Fornisce un'interfaccia grafica semplice basata su Tkinter e grafici generati con Matplotlib, con opzioni per personalizzare marker, linee, colori e limiti degli assi.

## Caratteristiche principali
- Importazione di dati da file CSV e XML.
- Interfaccia GUI con controlli per stile marker, tipo di linea, colore e limiti degli assi.
- Salvataggio delle configurazioni di plot.
- Moduli separati per creazione grafici, opzioni dati e opzioni di default.
- Supporto per lanciare l'app come script Python.

## Requisiti
- Python 3.8+
- Dipendenze Python: vedi requirements.txt (matplotlib, numpy, pandas, Pillow, scipy, ...)
- Pacchetto di sistema per GUI (su Debian/Ubuntu):
```
sudo apt update
sudo apt install python3-tk desktop-file-utils
```

Installa le dipendenze Python:
```
pip install -r requirements.txt
```

## Installazione
1. Vai alla cartella del progetto:
```
cd /home/simone/Scrivania/plotto-app
```
2. Installa le dipendenze Python:
```
pip install -r requirements.txt
```
3. Rendi eseguibili gli script (se necessario) e controlla gli script presenti:
```
chmod +x scripts/*.sh || true
ls -la scripts
```
4. Installa la voce del desktop (opzionale): usa lo script fornito che copia il file .desktop nella directory delle applicazioni e, se possibile, sul Desktop dell'utente:
```
./scripts/install_desktop_entry.sh
```
lo script copierà il file in:
- ${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto.desktop
e tenterà anche di copiare una copia su ~/Scrivania (se esiste).

5. Rendere eseguibile il file .desktop sulla Scrivania (se copiato lì):
- Tramite file manager: tasto destro sul file → Proprietà → Permessi → "Consenti l'esecuzione del file come programma".
- Tramite terminale:
```
chmod +x "$HOME/Scrivania/plotto.desktop"
```

6. Aggiungere l'app alla dock / barra delle applicazioni:
- Metodo consigliato (GNOME):
  - Dopo l'installazione apri "Attività" → cerca "Plotto" → apri l'app → tasto destro sull'icona nel dock → "Aggiungi ai preferiti".
- In alternativa copia il file .desktop in /usr/share/applications (richiede sudo) oppure modifica il file in ~/.local/share/applications e poi esegui:
```
update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
```
Nota: alcuni DE richiedono logout/login per mostrare la nuova voce.

Se vuoi che il .desktop punti esplicitamente all'icona presente nella cartella del progetto (src), modifica il campo Icon nel file .desktop:
```
sed -i "s|^Icon=.*|Icon=/home/simone/Scrivania/plotto-app/src/icona.png|" desktop/plotto.desktop
```
oppure dopo l'installazione modifica:
```
sed -i "s|^Icon=.*|Icon=${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto-app/icona.png|" "${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto.desktop"
```

Lo script di installazione può copiare anche PNG contenute in `src/` nella cartella di installazione (verifica `scripts/install_desktop_entry.sh`).

## Esecuzione
Puoi avviare l'app da dentro la cartella del progetto con uno dei due entrypoint presenti in `src`:
```
python3 src/main.py
# oppure
python3 src/app.py
```

## Icona finestra (Tkinter)
Per mostrare l'icona nella finestra dell'app il codice già cerca `icona.png` (o altri PNG) nella cartella `src/`. Se necessario metti `icona.png` in `src/` e l'app la userà automaticamente come iconphoto della finestra.

## Uso rapido
1. Avvia l'app.
2. Crea un nuovo grafico o apri un progetto esistente.
3. Carica un file CSV o XML contenente i dati.
4. Personalizza marker, linee, colori e limiti degli assi dal pannello di controllo.
5. Salva la configurazione se vuoi riutilizzarla.

## Formato dei dati suggerito
- CSV: prima riga con intestazioni, colonne numeriche per x e y.
- XML: struttura con nodi dati coerenti (vedere il codice in `src/data_options.py` per i dettagli del parsing).

## Risorse / immagini incluse (cartella src)
- src/cestino.png
- src/sfondo.png
- src/no_copyright.png
- src/icona.png

Se aggiungi o rinomini immagini in `src/`, aggiorna il file `desktop/plotto.desktop` o lo script di installazione per puntare alla nuova icona.

## Struttura del progetto (aggiornata)

/home/simone/Scrivania/plotto-app
├── src
│   ├── app.py
│   ├── create_plot.py
│   ├── data_options.py
│   ├── default_options.py
│   ├── main.py
│   ├── ui_elements.py
│   ├── cestino.png
│   ├── sfondo.png
│   ├── no_copyright.png
│   └── icona.png
├── desktop
│   └── plotto.desktop
├── scripts
│   └── install_desktop_entry.sh
├── README.md
├── requirements.txt
└── (altri file e cartelle)

## Debug e risoluzione problemi
- Se Tkinter non è disponibile: `sudo apt install python3-tk`.
- Se la voce non appare dopo l'installazione: esegui `update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications"` o riavvia la sessione.
- Per errori relativi alle immagini assicurati che i PNG siano presenti in `src/` o nella cartella in cui il .desktop punta.

## Contribuire
Apri una issue o invia una pull request. Aggiungi test e descrivi chiaramente le modifiche.

## Licenza
Aggiungi un file LICENSE per specificare la licenza del progetto.

## Contatti
Per domande o segnalazioni, apri una issue nel repository GitHub del progetto.