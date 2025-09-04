# Plotto App

**Plotto** è un’applicazione desktop scritta in Python per **visualizzare e analizzare dati** provenienti da file CSV e XML.  
Offre un’interfaccia grafica semplice (Tkinter) e grafici generati con Matplotlib, con opzioni di personalizzazione per marker, linee, colori e limiti degli assi.

---

## ✨ Caratteristiche principali
- Importazione di dati da file **CSV** e **XML**.  
- Interfaccia GUI intuitiva con controlli per:
  - stile dei marker  
  - tipo e colore delle linee  
  - limiti degli assi  
- Salvataggio e riutilizzo delle configurazioni di plot.  
- Architettura modulare: moduli separati per creazione grafici, gestione dei dati e opzioni di default.  
- Possibilità di avviare l’app direttamente come script Python.  

---

## 🛠️ Requisiti
- **Python 3.8+**  
- Dipendenze elencate in [`requirements.txt`](requirements.txt)  
  (inclusi `matplotlib`, `numpy`, `pandas`, `Pillow`, `scipy`, …)  

Per Debian/Ubuntu assicurati di avere i pacchetti GUI necessari:  
```bash
sudo apt update
sudo apt install python3-tk desktop-file-utils
```

Installa le dipendenze Python:  
```bash
pip install -r requirements.txt
```

---

## 🚀 Installazione
1. Clona o scarica il progetto ed entra nella cartella:
   ```bash
   cd /home/simone/Scrivania/plotto-app
   ```
2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```
3. Rendi eseguibili gli script (opzionale):
   ```bash
   chmod +x scripts/*.sh || true
   ls -la scripts
   ```
4. Installa la voce del menu desktop (opzionale):  
   ```bash
   ./scripts/install_desktop_entry.sh
   ```
   Lo script copierà `plotto.desktop` in:
   - `${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto.desktop`  
   - e, se esiste, anche in `~/Scrivania`.  

5. Se il file `.desktop` è stato copiato sul Desktop, rendilo eseguibile:
   ```bash
   chmod +x "$HOME/Scrivania/plotto.desktop"
   ```

6. Aggiungi Plotto al dock / barra delle applicazioni:
   - Metodo rapido (GNOME):  
     Apri **Attività → cerca "Plotto" → avvia → tasto destro → "Aggiungi ai preferiti"**.  
   - Metodo manuale: copia `plotto.desktop` in `/usr/share/applications` (richiede sudo) o aggiorna il database con:  
     ```bash
     update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
     ```

👉 Puoi modificare il campo `Icon=` del file `.desktop` per puntare a una tua icona personalizzata (ad esempio `src/icona.png`).  

---

## ▶️ Esecuzione
Da dentro la cartella del progetto:  
```bash
python3 src/main.py
# oppure
python3 src/app.py
```

---

## 🖼️ Icona finestra
L’app cercherà automaticamente un file `icona.png` (o altro PNG) nella cartella `src/` e lo userà come icona della finestra Tkinter.  
Se necessario, copia lì la tua icona.

---

## ⚡ Uso rapido
1. Avvia l’app.  
2. Crea un nuovo grafico o apri un progetto esistente.  
3. Carica un file CSV o XML con i tuoi dati.  
4. Personalizza marker, linee, colori e limiti degli assi.  
5. Salva la configurazione per riutilizzarla in futuro.  

---

## 📂 Formato dati consigliato
- **CSV**: prima riga con intestazioni, colonne numeriche per x e y.  
- **XML**: struttura con nodi dati coerenti (vedi parsing in `src/data_options.py`).  

---

## 🗂️ Risorse incluse (`src/`)
- `cestino.png`  
- `sfondo.png`  
- `no_copyright.png`  
- `icona.png`  

Se aggiungi/rinomini immagini, aggiorna anche `desktop/plotto.desktop` o lo script di installazione.

---

## 📁 Struttura del progetto
```
plotto-app/
├── src/
│   ├── app.py
│   ├── create_plot.py
│   ├── data_options.py
│   ├── default_options.py
│   ├── main.py
│   ├── ui_elements.py
│   ├── cestino.png
│   ├── sfondo.png
│   ├── no_copyright.png
│   └── icona_desktop.png
├── desktop/
│   └── plotto.desktop
├── scripts/
│   ├── install_desktop_entry.sh
│   └── run_plotto.sh
├── README.md
└── requirements.txt
```

---

## 🐞 Debug / Risoluzione problemi
- **Tkinter non disponibile** → `sudo apt install python3-tk`  
- **Voce menu non visibile** → esegui `update-desktop-database` o riavvia la sessione  
- **Errori con immagini** → assicurati che i PNG siano presenti in `src/` o nel percorso corretto indicato dal `.desktop`  

---

## 🤝 Contribuire
- Apri una **issue** o invia una **pull request**  
- Descrivi chiaramente le modifiche e, se possibile, includi test  

---

## 📜 Licenza
Aggiungi un file `LICENSE` per specificare la licenza del progetto.  

---

## 📬 Contatti
Per domande o segnalazioni, apri una **issue** nel repository GitHub del progetto.  