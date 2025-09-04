# Plotto App

## 🇮🇹 Versione Italiana

**Plotto** è un’applicazione desktop scritta in Python per **visualizzare e analizzare dati** provenienti da file CSV, XML e TXT.  
Offre un’interfaccia grafica semplice (Tkinter) e grafici generati con Matplotlib, con opzioni di personalizzazione per marker, linee, colori e limiti degli assi.

---

## ✨ Caratteristiche principali
- Importazione di dati da file **CSV**, **XML** e **TXT**.  
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

---

## ▶️ Esecuzione
Da dentro la cartella del progetto:  
```bash
python3 src/app.py
```
Altrimenti dall'icona sul desktop

---

## ⚡ Uso rapido
1. Avvia l’app.  
2. Crea un nuovo grafico o apri un progetto esistente.  
3. Carica un file CSV, XML o TXT con i tuoi dati.  
4. Personalizza marker, linee, colori e limiti degli assi.  
5. Salva la configurazione per riutilizzarla in futuro.  

---

## 📂 Formato dati consigliato
- **CSV**: prima riga con intestazioni, colonne numeriche per x e y.  
- **XML**: struttura con nodi dati coerenti (vedi parsing in `src/data_options.py`).  
- **TXT**: con la stessa struttura del CSV (può anche avere una tabulazione con lo spazio anziché ",")  

---

## 🗂️ Risorse incluse (`src/`)
- `cestino.png`  
- `sfondo.png`  
- `no_copyright.png`  
- `icona_desktop.png`  

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
Questo progetto è distribuito sotto licenza **CC0 1.0 Universal (Public Domain Dedication)**.  
Puoi copiare, modificare, distribuire ed eseguire l’opera, anche per fini commerciali, senza chiedere permesso.  

---

## 📬 Contatti
Per domande o segnalazioni, apri una **issue** nel repository GitHub del progetto.  


---

## 🇬🇧 English Version

**Plotto** is a desktop application written in Python to **visualize and analyze data** from CSV, XML, and TXT files.  
It provides a simple graphical interface (Tkinter) and plots generated with Matplotlib, with customization options for markers, lines, colors, and axis limits.

---

## ✨ Main Features
- Import data from **CSV**, **XML**, and **TXT** files.  
- Intuitive GUI with controls for:  
  - marker style  
  - line type and color  
  - axis limits  
- Save and reuse plot configurations.  
- Modular architecture: separate modules for plot creation, data management, and default options.  
- Can be launched directly as a Python script.  

---

## 🛠️ Requirements
- **Python 3.8+**  
- Dependencies listed in [`requirements.txt`](requirements.txt)  
  (including `matplotlib`, `numpy`, `pandas`, `Pillow`, `scipy`, …)  

On Debian/Ubuntu make sure you have the necessary GUI packages:  
```bash
sudo apt update
sudo apt install python3-tk desktop-file-utils
```

Install Python dependencies:  
```bash
pip install -r requirements.txt
```

---

## 🚀 Installation
1. Clone or download the project and navigate into the folder:
   ```bash
   cd /home/simone/Scrivania/plotto-app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make scripts executable (optional):
   ```bash
   chmod +x scripts/*.sh || true
   ls -la scripts
   ```
4. Install desktop entry (optional):  
   ```bash
   ./scripts/install_desktop_entry.sh
   ```
   The script will copy `plotto.desktop` to:
   - `${XDG_DATA_HOME:-$HOME/.local/share}/applications/plotto.desktop`  
   - and, if available, also to `~/Desktop`.  

5. If the `.desktop` file was copied to your Desktop, make it executable:
   ```bash
   chmod +x "$HOME/Desktop/plotto.desktop"
   ```

6. Add Plotto to the dock / application bar:
   - Quick method (GNOME):  
     Open **Activities → search "Plotto" → run → right-click the icon → "Add to Favorites"**.  
   - Manual method: copy `plotto.desktop` into `/usr/share/applications` (requires sudo) or update the database with:  
     ```bash
     update-desktop-database "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
     ```

---

## ▶️ Run
From inside the project folder:  
```bash
python3 src/app.py
```
Or simply launch it from the desktop icon.

---

## ⚡ Quick Usage
1. Launch the app.  
2. Create a new plot or open an existing project.  
3. Load a CSV, XML, or TXT file with your data.  
4. Customize markers, lines, colors, and axis limits.  
5. Save the configuration for future use.  

---

## 📂 Recommended Data Format
- **CSV**: first row as headers, numeric columns for x and y.  
- **XML**: structured nodes with consistent data (see parsing in `src/data_options.py`).  
- **TXT**: same structure as CSV (may use space/tab instead of commas).  

---

## 🗂️ Included Resources (`src/`)
- `cestino.png`  
- `sfondo.png`  
- `no_copyright.png`  
- `icona_desktop.png`  

If you add/rename images, also update `desktop/plotto.desktop` or the installation script.

---

## 📁 Project Structure
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

## 🐞 Debug / Troubleshooting
- **Tkinter not available** → `sudo apt install python3-tk`  
- **Menu entry not visible** → run `update-desktop-database` or restart your session  
- **Image-related errors** → ensure PNGs are in `src/` or in the path pointed by `.desktop`  

---

## 🤝 Contributing
- Open an **issue** or submit a **pull request**  
- Clearly describe your changes and, if possible, include tests  

---

## 📜 License
This project is licensed under **CC0 1.0 Universal (Public Domain Dedication)**.  
You can copy, modify, distribute, and perform the work, even for commercial purposes, without asking permission.  

---

## 📬 Contact
For questions or bug reports, please open an **issue** in the GitHub repository.  