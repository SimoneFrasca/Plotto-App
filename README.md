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
- Dipendenze comuni: tkinter, matplotlib, pandas, lxml (verifica requirements.txt se presente)

Installa le dipendenze:
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
4. Installa la voce del desktop (opzionale): usa lo script fornito che copia il file .desktop nella directory delle applicazioni e (se presente) sul Desktop dell'utente:
```
./scripts/install_desktop_entry.sh
```
5. Rendi eseguibile il programma cliccando sull'icona con il tasto destro
```
Lo script installerà il file in "${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto.desktop" e tenterà di copiarlo anche nella directory Desktop dell'utente (es. ~/Scrivania). Potrebbe essere necessario eseguire `update-desktop-database` o riavviare la sessione per vedere la voce nel menu.

Note:
- Su Debian/Ubuntu è necessario il pacchetto di sistema per Tkinter:
```
sudo apt update
sudo apt install python3-tk
```
- Se lo script richiede permessi aggiuntivi, eseguilo dall'utente corrente (non usare sudo a meno che tu non voglia installare globalmente).
- Verifica il contenuto della cartella `scripts` per eventuali altri script di utilità (es. script per avviare

## Esecuzione
Puoi avviare l'app da dentro la cartella del progetto con uno dei due entrypoint presenti in src:
```
python3 src/main.py
# oppure
python3 src/app.py
```

## Uso rapido
1. Avvia l'app.
2. Crea un nuovo grafico o apri un progetto esistente.
3. Carica un file CSV o XML contenente i dati.
4. Personalizza marker, linee, colori e limiti degli assi dal pannello di controllo.
5. Salva la configurazione se vuoi riutilizzarla.

## Formato dei dati suggerito
- CSV: prima riga con intestazioni, colonne numeriche per x e y.
- XML: struttura con nodi dati coerenti (vedere il codice in src per dettagli sul parsing).

## Struttura del progetto (aggiornata)
```
/home/simone/Scrivania/plotto-app
├── src
│   ├── app.py                # Interfaccia e logica di alto livello
│   ├── create_plot.py        # Funzioni di creazione del grafico (Matplotlib)
│   ├── data_options.py       # Parsing e opzioni relative ai dati
│   ├── default_options.py    # Opzioni di default per i plot
│   ├── main.py               # Entry point / avvio dell'app
│   └── ui_elements.py        # Componenti GUI riutilizzabili
│   └── cestino.png        
│   └── sfondo.png        
│   └── no_copyright.png        
│   └── icona.png        
├── README.md
├── requirements.txt (se presente)
└── (altri file e cartelle: scripts, desktop, ecc. — verifica il repo)
```

## Debug e risoluzione problemi
- Se Tkinter non è disponibile: `sudo apt install python3-tk`.
- Esegui lo script dall'interno della cartella del progetto e controlla l'output nel terminale integrato di VS Code per eventuali errori.
- Per problemi di parsing CSV/XML, verifica l'encoding e il formato delle intestazioni o controlla le funzioni in `src/data_options.py`.

## Contribuire
Apri una issue o invia una pull request. Aggiungi test e descrivi chiaramente le modifiche.

## Licenza
Specifica la licenza aggiungendo un file LICENSE nel repository.

## Contatti
Per domande o segnalazioni, apri una issue nel repository GitHub del progetto.