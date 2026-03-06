from fileinput import filename
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
from ui_elements import dim, convert_file_to_csv, ToolTip
from default_options import GeneralOptions, LegendOptions, FontOptions, LatexConvert, SubplotOptions, Constant
from default_options import  DefaultPlot, DefaultHist, DefaultScatter, DefaultBar
from default_options import DefaultPie, DefaultBoxPlot, DefaultViolin, DefaultHeatmap
from default_options import DefaultContour, DefaultQuiver, DefaultPolar, DefaultStack
from data_options import DataOptions, InsetOptions, InsertFunction
from create_plot import CreatePlot
import json

LABEL_FONT = dim.label_font()
ENTRY_FONT = dim.entry_font()

class MainPage(tk.Frame):
    def __init__(self, DataPlotterApp, master, upload_configuration=False):
        self.dataplotter = DataPlotterApp
        self.master = master
        
        self.active_subplot_id = None
        self.subplot_states = {}  # Inizialmente vuoto
        self.subplot_id = []
        self.subplot_counter = 1
        
        # AGGIUNGI QUESTI: servono come "contenitori" per lo switch
        self.data_id = []
        self.inset_id = ["inset_0"]
        self.function_id = []
        self.data_options = {}
        self.inset_options = {}
        self.function_options = {}
        self.data_counter = [0]
        self.function_counter = [0]
        self.inset_counter = 1
        
        
        self.general_options = {    
            "structure": GeneralOptions().general_opt,
            "font": FontOptions().font_options,
        }
        self.default_options = {
            "plot": DefaultPlot().default_plot,
            "hist": DefaultHist().hist,
            "scatter": DefaultScatter().scatter,
            "bar": DefaultBar().bar,
            "pie": DefaultPie().pie,
            "boxplot": DefaultBoxPlot().box,
            "violin": DefaultViolin().violin,
            "heatmap": DefaultHeatmap().heatmap,
            "contour": DefaultContour().contour,
            "quiver": DefaultQuiver().quiver,
            "polar": DefaultPolar().polar,
            "stack": DefaultStack().stack,
        }
        
        self.columns = {}

        # Clear previous widgets
        for widget in master.winfo_children():
            widget.destroy()
        super().__init__(master)
        master.title("Plotto")
        master.geometry("800x500")
        master.attributes('-zoomed', True)

        # Configure main grid
        master.grid_rowconfigure(0, weight=0)
        master.grid_rowconfigure(1, minsize=0, weight=0)
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # Main menu bar
        self.menu_bar_frame = tk.Frame(master, bg="white")
        self.menu_bar_frame.grid(row=0, column=0, sticky="ew")

        # Create the menu content frame before passing it to MenuToggleManager
        self.menu_frame = tk.Frame(master, bg="white")
        self.menu_frame.grid(row=1, column=0, sticky="ew")
        self.menu_frame.grid_remove()
                
        self.menu_content_frame = tk.Frame(self.menu_frame, bg="white")
        self.menu_content_frame.grid(row=0, column=0, sticky="ew")
        self.menu_content_frame.grid_remove()  # Hidden initially
        # -------------------------------------

        # Default options menu frame
        self.menu_default_frame = tk.Frame(self.menu_frame, bg="white")
        self.menu_default_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.menu_default_frame.grid_remove()  # Initially hidden

        # Correct construction order!
        self.toggle_manager = MenuToggleManager(self, self.general_options, self.default_options)

        # Now continue with the rest of your initialization...
        # (e.g., self.menu_bar, self.default_buttons, creation of main_frame, etc.)

        # Main button bar
        self.menu_bar(master, self.menu_bar_frame)
        # Default buttons bar
        self.default_buttons(self.menu_default_frame)

        # -----------------------------------------------------------------------------------------------------
        
        # Main frame
        
        # 1. IL FRAME PRINCIPALE DEI SUBPLOT
        self.subplot_frame = tk.Frame(master, bg="lightgrey", relief=tk.SUNKEN, borderwidth=1)
        self.subplot_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5) 
        master.grid_rowconfigure(2, weight=0)

        # Usiamo la griglia anche dentro subplot_frame per gestire i due livelli
        self.subplot_frame.grid_columnconfigure(0, weight=1)

        # 2. SOTTOTELAIO PER I BOTTONI (La riga con "Add Subplot" e i vari "Subplot_1...")
        self.subplot_buttons_container = tk.Frame(self.subplot_frame, bg="lightgrey")
        self.subplot_buttons_container.grid(row=0, column=0, sticky="w")

        # Il bottone "Add subplot" ora va dentro il container
        self.add_btn = tk.Button(self.subplot_buttons_container, text="Add subplot",
                command=self.on_add_subplot_click, font=LABEL_FONT)
        self.add_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 3. IL FRAME DELLE OPZIONI (Proprio sotto i bottoni, nello stesso subplot_frame)
        self.subplot_options_frame = tk.Frame(self.subplot_frame, bg="white", relief=tk.RIDGE, borderwidth=1)
        self.subplot_options_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.subplot_options_frame.grid_remove() # Nascosto all'inizio
        
        # -----------------------------------------------------------------------------------------------------
        
        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        master.grid_rowconfigure(3, weight=1)

        self.main_frame.grid_columnconfigure(0, weight=3)  # Scrollable menu column
        self.main_frame.grid_columnconfigure(1, weight=1)  # Right-side windows column
        self.main_frame.grid_rowconfigure(0, weight=3)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # Left column: scrollable menu
        self.data_menu_frame = tk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=1)
        self.data_menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=2)

        self.data_menu_frame.grid_rowconfigure(0, weight=1)
        self.data_menu_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.data_menu_frame)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.data_menu_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        tk.Button(self.scrollable_frame, text="Add file",
          command=lambda: self.add_file(self.scrollable_frame,0),
          font=LABEL_FONT).pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
        
        # -----------------------------------------------------------------------------------------------------

        # Left column: scrollable inset menu
        self.menu_frame_inset = tk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=1)
        self.menu_frame_inset.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.menu_frame_inset.grid_remove()

        self.menu_frame_inset.grid_rowconfigure(0, weight=1)
        self.menu_frame_inset.grid_columnconfigure(0, weight=1)

        self.canvas_inset = tk.Canvas(self.menu_frame_inset)
        self.canvas_inset.grid(row=0, column=0, sticky="nsew")

        scrollbar_inset = ttk.Scrollbar(self.menu_frame_inset, orient="vertical", command=self.canvas_inset.yview)
        scrollbar_inset.grid(row=0, column=1, sticky="ns")
        self.canvas_inset.configure(yscrollcommand=scrollbar_inset.set)

        self.scrollable_inset_frame = tk.Frame(self.canvas_inset)
        self.canvas_inset.create_window((0, 0), window=self.scrollable_inset_frame, anchor="nw")
        self.scrollable_inset_frame.bind(
            "<Configure>",
            lambda e: self.canvas_inset.configure(scrollregion=self.canvas_inset.bbox("all"))
        )
        tk.Button(self.scrollable_inset_frame, text="Add inset",
                  command=self.add_inset, font=LABEL_FONT).pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
        
        # --------------------------------------------------------------------------------------------------
        # Right column: two vertical windows
        function_frame = tk.Frame(self.main_frame,bg="lightblue",relief=tk.SUNKEN,borderwidth=1,width=600,height=400)
        function_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        function_frame.pack_propagate(False)  # Prevent resizing with content
        
        function_frame.grid_rowconfigure(0, weight=1)
        function_frame.grid_columnconfigure(0, weight=1)

        self.canvas_function = tk.Canvas(function_frame,bg="lightblue")
        self.canvas_function.grid(row=0, column=0, sticky="nsew")

        scrollbar_function = ttk.Scrollbar(function_frame, orient="vertical", command=self.canvas_function.yview)
        scrollbar_function.grid(row=0, column=1, sticky="ns")
        self.canvas_function.configure(yscrollcommand=scrollbar_function.set)

        self.scrollable_function_frame = tk.Frame(self.canvas_function)
        self.canvas_function.create_window((0, 0), window=self.scrollable_function_frame, anchor="nw")
        self.scrollable_function_frame.bind(
            "<Configure>",
            lambda e: self.canvas_function.configure(scrollregion=self.canvas_function.bbox("all"))
        )
        tk.Button(self.scrollable_function_frame, text="Add function",
                  command=lambda: self.add_function(self.scrollable_function_frame, 0), font=LABEL_FONT).pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)

        # --------------------------------------------------------------------------------------------------
        # In the constructor, after creating self.plot_window_frame
        self.plot_window_frame = tk.Frame(
            self.main_frame,
            bg="lightgreen",
            relief=tk.SUNKEN,
            borderwidth=1,
            width=600,   # fixed width in pixels
            height=400   # fixed height in pixels
        )
        self.plot_window_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.plot_window_frame.grid_propagate(False)  # Prevent the frame from resizing with content
        
        self.plot_button_frame = tk.Frame(self.plot_window_frame, bg="lightgreen")
        self.plot_button_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        plot = tk.Button(self.plot_button_frame, text="Plot", font=LABEL_FONT,
                  command=lambda: self.submit_data())
        plot.grid(row=0, column=0, padx=2, pady=2)
        ToolTip(plot, "Plot the data with the current configuration")
        show_plot = tk.Button(self.plot_button_frame, text="Show Plot", font=LABEL_FONT,
                  command=lambda: self.submit_data(show=True))
        show_plot.grid(row=0, column=1, padx=2, pady=2)
        ToolTip(show_plot, "Show the plot in a new window")
        save_plot = tk.Button(self.plot_button_frame, text="Save Plot", font=LABEL_FONT,
                  command=lambda: self.submit_data(save=True))
        save_plot.grid(row=0, column=2, padx=2, pady=2)
        ToolTip(save_plot, "Save the plot as a file")
        # --------------------------------------------------------------------------------------------------


        if not upload_configuration:
            self.on_add_subplot_click()
        else:
            # 1. Carica i dati dal file nel dizionario subplot_states
            self.upload()
            
            # 2. Ora iteriamo correttamente. 
            # Dobbiamo usare .values() per avere l'oggetto stato, non solo il nome
            for sid in self.subplot_id:
                
                # Creiamo il bottone e l'interfaccia per questo subplot
                state = self.subplot_states[sid]
                print("\n\nSubplot caricato:", state["subplot_id"])
                
                # Sincronizziamo i puntatori della classe con lo stato appena letto
                print("inset_id:", state["inset_id"])
                
                self.active_subplot_id = state["subplot_id"]
                self.data_id = state["data_id"]
                self.inset_id = state["inset_id"]
                self.function_id = state["function_id"]
                
                self.on_add_subplot_click(subplot_id=sid, upload=True)
            
                self.data_options = state["data_options"]
                self.inset_options = state["inset_options"]
                self.function_options = state["function_options"]
                self.columns = state["columns"]
                self.data_counter = state["data_counter"]
                self.function_counter = state["function_counter"]
                self.inset_counter = state["inset_counter"]
                
                # 3. Ricostruzione grafica degli Inset
                for inset_id in self.inset_id:
                    if inset_id != "inset_0":
                        # Se l'inset esiste, mostriamo il frame e lo aggiungiamo
                        self.add_inset_frame()
                        # split('_')[-1] serve a recuperare l'indice numerico (es. "0" da "inset_0")
                        idx = int(inset_id.split('_')[-1])
                        self.add_inset(upload=True, inset_id=inset_id, inset_index=idx)
                
                # 4. Ricostruzione grafica dei File
                for data_id in self.data_id:
                    # Carichiamo i file che appartengono all'inset 0 (quello principale)
                    if self.data_options[data_id]['inset'] == 0:
                        path = self.data_options[data_id]['file path']
                        self.add_file(self.scrollable_frame, 0, data_id, path, upload=True)
                        
                # 5. Ricostruzione grafica delle Funzioni
                for function_id in self.function_id:
                    if self.function_options[function_id]['inset'] == 0:
                        self.add_function(self.scrollable_function_frame, 0, function_id, upload=True)


            self._refresh_workspace_gui()
            messagebox.showinfo("Upload completed", f"Configuration uploaded.")
            upload_configuration = False


    def menu_bar(self, master, frame):
        master.grid_columnconfigure(0, weight=1)
        tk.Button(frame, text="File", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("file")).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame, text="General Options", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("opzioni_gen")).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame, text="Font", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("opzioni_font")).grid(row=0, column=2, padx=2, pady=2)
        tk.Button(frame, text="Default Plot Options", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("default")).grid(row=0, column=3, padx=2, pady=2)
        tk.Button(frame, text="Latex → Numpy converter", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("latex_convert")).grid(row=0, column=4, padx=2, pady=2)
        tk.Button(frame, text="Constant", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("constant")).grid(row=0, column=5, padx=2, pady=2)


        
    def on_add_subplot_click(self, subplot_id=None, upload=False):
        sid = subplot_id
        
        if not upload:
            # Logica del contatore (già esistente)
            if self.subplot_id:
                numeri = [int(s.split('_')[-1]) for s in self.subplot_id if '_' in s]
                self.subplot_counter = max(numeri) + 1 if numeri else 1
            else:
                self.subplot_counter = 1
            
            sid = f"Subplot_{self.subplot_counter}"
            self.subplot_id.append(sid)
            self.subplot_states[sid] = {
                "subplot_id": sid,
                "structure": SubplotOptions().general_opt,
                "legend": LegendOptions().legend,
                "inset_frame_visible": False,
                "data_id": [],
                "inset_id": ["inset_0"],
                "function_id": [],
                "data_options": {},
                "inset_options": {},
                "function_options": {},
                "columns": {},
                "data_counter": [0],
                "function_counter": [0],
                "inset_counter": 1
            }
            
        # --- NUOVA LOGICA: CONTAINER PER IL SUBPLOT ---
        # Creiamo un frame che si comporta come un pulsante
        container = tk.Frame(self.subplot_buttons_container, bg="white", 
                             highlightbackground="grey", highlightthickness=1)
        container.pack(side=tk.LEFT, padx=2, pady=5)

        # Label con il nome (cliccarla attiva lo switch)
        lbl = tk.Label(container, text=sid, font=LABEL_FONT, bg="white", padx=5)
        lbl.pack(side=tk.LEFT)
        lbl.bind("<Button-1>", lambda e, s=sid: self.switch_subplot(s))

        def on_enter(e): 
            if container["bg"] != "#04d415": # Solo se non è quello attivo
                container.configure(bg="#f0f0f0")
                lbl.configure(bg="#f0f0f0")

        def on_leave(e):
            if container["bg"] != "#04d415":
                container.configure(bg="white")
                lbl.configure(bg="white")

        lbl.bind("<Enter>", on_enter)
        lbl.bind("<Leave>", on_leave)
        container.bind("<Enter>", on_enter)
        container.bind("<Leave>", on_leave)

        # Bottoncino X per eliminare
        del_btn = tk.Button(container, text="×", font=("Arial", 8, "bold"), 
                            fg="red", bg="white", relief=tk.FLAT,
                            command=lambda s=sid, c=container: self.delete_subplot(s, c))
        del_btn.pack(side=tk.LEFT, padx=(0, 2))

        # Salviamo il riferimento al container nel dizionario dello stato (opzionale ma utile)
        self.subplot_states[sid]["button_widget"] = container
    
        self.switch_subplot(sid)
        

    def switch_subplot(self, sid):
        # ... dopo la sincronizzazione dei puntatori ...
        print(f"\n[SWITCH] Attivato: {sid}")
        print(f"DEBUG: ID lista data_id in memoria: {id(self.data_id)}") 
        print(f"DEBUG: Elementi attuali in questo subplot: {self.data_id}")
        print(f"Subplot attivo in questo momento: {self.active_subplot_id}")
        
        
        # --- GESTIONE ESTETICA BOTTONI (CONTAINER) ---
        for container in self.subplot_buttons_container.winfo_children():
            # Cerchiamo la Label dentro il container per capire quale subplot è
            # Assumiamo che la Label sia il primo figlio (index 0) o cerchiamola per tipo
            current_label = None
            for child in container.winfo_children():
                if isinstance(child, tk.Label):
                    current_label = child
                    break
            
            if current_label:
                if current_label.cget("text") == sid:
                    # Colore ATTIVO (Verde)
                    container.configure(bg="#04d415")
                    current_label.configure(bg="#04d415")
                else:
                    # Colore INATTIVO (Bianco)
                    container.configure(bg="white")
                    current_label.configure(bg="white")
                    
        # Se clicco sul subplot GIÀ ATTIVO -> Toggle del nuovo frame opzioni
        if self.active_subplot_id == sid:
            print(f"{sid}={self.active_subplot_id}")
            self._toggle_subplot_options(sid)
            return

        # --- CAMBIO AMBIENTE ---
        self.active_subplot_id = sid
        state = self.subplot_states[sid]
        
        # Sincronizzazione puntatori
        self.data_id = state["data_id"]
        self.inset_id = state["inset_id"]
        self.function_id = state["function_id"]
        self.data_options = state["data_options"]
        self.inset_options = state["inset_options"]
        self.function_options = state["function_options"]
        self.columns = state["columns"]
        self.data_counter = state["data_counter"]
        self.function_counter = state["function_counter"]
        self.inset_counter = state["inset_counter"]

        # Aggiorna UI file e funzioni
        self._refresh_workspace_gui()
        # ... (codice esistente) ...
        print(f"[GUI REFRESH] Ricostruzione completata per {self.active_subplot_id}")
        print(f"   -> File: {len(self.data_id)}, Funzioni: {len(self.function_id)}, Inset: {len(self.inset_id)-1}")
        
    
        # Mostra il pannello strumenti
        self._toggle_subplot_options(sid, force_open=True)

    def _toggle_subplot_options(self, sid, force_open=False):
        if self.subplot_options_frame.winfo_viewable() and not force_open:
            self.subplot_options_frame.grid_remove()
        else:
            self.subplot_options_frame.grid()
            for widget in self.subplot_options_frame.winfo_children():
                widget.destroy()
            
            # --- 1. CONFIGURA IL PADRE DI TUTTI ---
            # Forza il frame contenitore a prendersi tutto lo spazio orizzontale disponibile
            self.subplot_options_frame.grid_columnconfigure(0, weight=1)

            options_content_frame = tk.Frame(self.subplot_options_frame, bg="white")
            # Fondamentale: sticky="nsew" per riempire lo spazio dato dal columnconfigure sopra
            options_content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

            # --- 2. CONFIGURA LE COLONNE INTERNE ---
            # Qui diamo peso 3 alla prima colonna e 1 alla terza
            options_content_frame.grid_columnconfigure(0, weight=3) 
            options_content_frame.grid_columnconfigure(1, weight=0) # Separatore (non deve espandersi)
            options_content_frame.grid_columnconfigure(2, weight=1) 

            # --- 2a. OPZIONI STRUTTURA SUBPLOT ---
            struct_label = tk.Label(options_content_frame, text="Subplot Structure", font=LABEL_FONT, bg="white", fg="blue")
            struct_label.grid(row=0, column=0, sticky="w")
            
            subplot_struct_inner = tk.Frame(options_content_frame, bg="white")
            # sticky="nsew" è vitale qui per far sì che il frame occupi la colonna 0 allargata
            subplot_struct_inner.grid(row=1, column=0, sticky="nsew")
            
            # CHIAMATA IMPORTANTE:
            SubplotOptions().options(subplot_struct_inner, self.subplot_states[sid]["structure"])

            # --- SEPARATORE ---
            tk.Frame(options_content_frame, width=1, bg="grey").grid(row=0, column=1, rowspan=2, sticky="ns", padx=10)

            # --- 2b. OPZIONI LEGENDA ---
            legend_label = tk.Label(options_content_frame, text="Legend Configuration", font=LABEL_FONT, bg="white", fg="blue")
            legend_label.grid(row=0, column=2, sticky="w")
            
            legend_inner = tk.Frame(options_content_frame, bg="white")
            legend_inner.grid(row=1, column=2, sticky="nsew")
            LegendOptions().options(legend_inner, self.subplot_states[sid]["legend"])

    def _refresh_workspace_gui(self):
        """Pulisce l'interfaccia e ricrea i widget basandosi sullo stato del subplot attivo."""
        
        # 1. SVUOTA TUTTI I FRAME
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for widget in self.scrollable_function_frame.winfo_children():
            widget.destroy()
        for widget in self.scrollable_inset_frame.winfo_children(): # SVUOTA ANCHE GLI INSET
            widget.destroy()

        # 2. GESTIONE VISIBILITÀ INSET FRAME
        # Controlla se il subplot attivo aveva l'inset frame aperto
        if self.subplot_states[self.active_subplot_id].get("inset_frame_visible", False):
            self.add_inset_frame()
        else:
            self.remove_inset_frame()

        # 3. RICREA I BOTTONI "ADD"
        add_buttons_container = tk.Frame(self.scrollable_frame, bg="white")
        add_buttons_container.pack(fill=tk.X, padx=5, pady=5)
        # Bottone Add File (a sinistra)
        tk.Button(add_buttons_container, text="Add file",
                command=lambda: self.add_file(self.scrollable_frame, 0),
                font=LABEL_FONT).pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)

        # Bottone Add Inset (a destra)
        tk.Button(add_buttons_container, text="Add Inset", 
                font=LABEL_FONT,
                command=lambda: self.add_inset_frame(),
                bg="#e1e1e1").pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        tk.Button(self.scrollable_function_frame, text="Add function",
                command=lambda: self.add_function(self.scrollable_function_frame, 0),
                font=LABEL_FONT).pack(padx=5, pady=5, fill=tk.X)
                
        tk.Button(self.scrollable_inset_frame, text="Add inset", # REINSERISCI BOTTONE INSET
                  command=self.add_inset, font=LABEL_FONT).pack(padx=5, pady=5, fill=tk.X)

        # 4. RICOSTRUISCI GLI INSET ESISTENTI PER QUESTO SUBPLOT
        # Saltiamo inset_0 perché è quello principale (già gestito dai bottoni sopra)
        for i_id in self.inset_id:
            if i_id != "inset_0":
                # Ricreiamo l'oggetto grafico InsetOptions
                # Nota: add_inset deve gestire il parametro upload=True per non incrementare contatori
                self.add_inset(upload=True, inset_id=i_id, inset_index=int(i_id.split('_')[1]))

        # 5. RICOSTRUISCI FILE E FUNZIONI (il tuo codice esistente...)
        for d_id in self.data_id:
            # Assicurati che add_file venga chiamato sul frame corretto 
            # (se il file appartiene a un inset, deve andare nel frame dell'inset)
            # Per semplicità qui gestiamo quelli dell'inset principale (0)
            if self.data_options[d_id]['inset'] == 0:
                path = self.data_options[d_id]['file path']
                self.add_file(self.scrollable_frame, 0, data_id=d_id, file_path=path, upload=True)

        for f_id in self.function_id:
            if self.function_options[f_id]['inset'] == 0:
                self.add_function(self.scrollable_function_frame, 0, function_id=f_id, upload=True)
        
        
    def delete_subplot(self, sid, container_widget):
        # Chiedi conferma
        if not messagebox.askyesno("Delete Subplot", f"Are you sure you want to delete {sid}?"):
            return

        # 1. Rimuovi dai dati
        if sid in self.subplot_id:
            self.subplot_id.remove(sid)
        if sid in self.subplot_states:
            del self.subplot_states[sid]

        # 2. Distruggi l'elemento grafico
        container_widget.destroy()

        # 3. Gestisci lo switch se abbiamo eliminato il subplot attivo
        if self.active_subplot_id == sid:
            self.subplot_options_frame.grid_remove() # Chiudi le opzioni
            if self.subplot_id:
                # Passa all'ultimo subplot rimasto
                self.switch_subplot(self.subplot_id[-1])
            else:
                # Se non ce ne sono più, pulisci tutto
                self.active_subplot_id = None
                self._refresh_workspace_gui()
        
        
        
        
        
        
    
    def add_inset_frame(self):
        # Mostra graficamente i frame
        self.data_menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        self.menu_frame_inset.grid()
        
        # Registra nello stato del subplot attivo che l'inset frame è aperto
        # (Aggiungi questa chiave nel dizionario in on_add_subplot_click)
        if self.active_subplot_id:
            self.subplot_states[self.active_subplot_id]["inset_frame_visible"] = True
        
    def remove_inset_frame(self):
        self.data_menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=2)
        self.menu_frame_inset.grid_remove() 
        
    def default_buttons(self, frame):
        default_buttons = [
            ("Plot", "plot"),
            ("Histogram", "hist"),
            ("Scatter", "scatter"),
            ("Bar", "bar"),
            ("Pie", "pie"),
            ("BoxPlot", "boxplot"),
            ("Violin", "violin"),
            ("Heatmap", "heatmap"),
            ("Contour", "contour"),
            ("Quiver", "quiver"),
            ("Polar", "polar"),
            ("Stack", "stack")
        ]
        for idx, (name, key) in enumerate(default_buttons):
            tk.Button(frame, text=f"Default {name}", font=LABEL_FONT,
                      command=lambda k=key: self.toggle_manager.toggle(k)).grid(row=0, column=idx)
   
    def add_file(self, frame, inset_counter,data_id=None, file_path=None, upload=False):
        if self.active_subplot_id is None:
            messagebox.showwarning("Attenzione", "Crea o seleziona un Subplot prima di aggiungere file!")
            return
        if not upload:
            file_path = filedialog.askopenfilename(
                title="Seleziona un file",
                filetypes=[("CSV Files", "*.csv"), ("XML Files", "*.xml"), ("Text Files", "*.txt")]
            )
            if not file_path:
                return
            data_id = f"{self.active_subplot_id}_inset_{inset_counter}_data_{int(self.data_counter[inset_counter])}"
            print(f"[ADD FILE] Subplot: {self.active_subplot_id} | Inset: {inset_counter} | ID Generato: {data_id}")
            while data_id in self.data_id:  
                self.data_counter[inset_counter] += 1
                data_id = f"{self.active_subplot_id}_inset_{inset_counter}_data_{int(self.data_counter[inset_counter])}"
            self.data_id.append(data_id)

        try:
            if file_path.endswith('.txt'):
                csv_path = convert_file_to_csv(file_path)
                df = pd.read_csv(csv_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xml'):
                df = pd.read_xml(file_path)
            else:
                messagebox.showerror("Error", "Unsupported file format.")
                return
            # Salva colonne specifiche del file
            self.columns[data_id] = df.columns.tolist()

            DataOptions(frame,
                        inset_counter,
                        data_id,
                        file_path,
                        self.columns[data_id],
                        self.data_options,
                        self.data_id,
                        upload
                    )
            
            print(f"File caricato: {data_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Loading Error:\n{e}")

    def add_function(self, frame, inset_counter, function_id = None, upload = False):
        if self.active_subplot_id is None:
            messagebox.showwarning("Attenzione", "Crea o seleziona un Subplot prima di aggiungere file!")
            return
        if not upload:
            function_id = f"{self.active_subplot_id}_inset_{inset_counter}_function_{int(self.function_counter[inset_counter])}"
            print(f"[ADD FUNCTION] Subplot: {self.active_subplot_id} | Inset: {inset_counter} | ID Generato: {function_id}")
            while function_id in self.function_id:  
                self.function_counter[inset_counter] += 1
                function_id = f"{self.active_subplot_id}_inset_{inset_counter}_function_{int(self.function_counter[inset_counter])}"
            self.function_id.append(function_id)

        InsertFunction(frame, inset_counter, function_id, self.function_options, self.function_id, upload)
        
    def add_inset(self,upload=False,inset_id=None,inset_index=None):
        if self.active_subplot_id is None:
            messagebox.showwarning("Attenzione", "Crea o seleziona un Subplot prima di aggiungere file!")
            return
        frame = tk.Frame(self.scrollable_inset_frame, relief=tk.SUNKEN, borderwidth=2)
        frame.pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
        if not upload:
            inset_index = self.inset_counter  # salva valore attuale
            # Aggiorna inset_id e contatore
            inset_id = f"{self.active_subplot_id}_inset_{inset_index}"
            print(f"[ADD INSET] Subplot: {self.active_subplot_id} | ID Generato: {inset_id}")
            self.inset_id.append(inset_id)
            self.inset_counter += 1  # incrementa per il prossimo inset                 
        
        obj = InsetOptions(frame, inset_index, inset_id,  self.inset_options, self.inset_id, self, upload)
        self.inset_options[inset_id] = obj.inset_opt
        
        self.data_counter.append(0)  # aggiungi contatore per questo inset
        self.function_counter.append(0)  # aggiungi contatore per questo inset
        
        buttons_frame = tk.Frame(frame)
        buttons_frame.pack(pady=dim.s(5))  # questo frame è centrato nel parent
        
        if upload:
            for data_id in self.data_id:
                if (self.data_options[data_id]['inset']) == inset_index:
                    self.add_file(frame, inset_index, data_id, self.data_options[data_id]['file path'], True)
                    
            for function_id in self.function_id:
                if (self.function_options[function_id]['inset']) == inset_index:
                    self.add_function(frame, inset_index, function_id, True)

        tk.Button(
            buttons_frame,
            text="Add file",
            command=lambda idx=inset_index: self.add_file(frame, idx),
            font=LABEL_FONT
        ).pack(side="left", padx=dim.s(10))

        tk.Button(
            buttons_frame,
            text="Add function",
            command=lambda idx=inset_index: self.add_function(frame, idx),
            font=LABEL_FONT
        ).pack(side="left", padx=dim.s(10))

    def submit_data(self,save=None, show=None):
        # Gestisce il submit dei dati per il plot
        if not self.data_id and not self.function_id:
            messagebox.showwarning("Warning", "No files loaded")
            return

        # Distruggi frame precedente se esiste
        if hasattr(self, "plot_frame") and self.plot_frame.winfo_exists():
            self.plot_frame.destroy()

        # Crea nuovo frame
        self.plot_frame = tk.Frame(self.plot_window_frame)
        self.plot_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=0)

        # Crea plot
        self.create_plot = CreatePlot(
            self.plot_frame,
            self.subplot_states,
            self.subplot_id,
            self.general_options,
            self.default_options,
            self.data_options,
            self.inset_options,
            self.function_options,
            self.data_id,
            self.inset_id,
            self.function_id,
            save,
            show
        )
        
        if save:
            plot = tk.Button(self.plot_button_frame, text="Show saved plot", font=LABEL_FONT,
                    command=lambda: self.create_plot.show_saved_file())
            plot.grid(row=0, column=3, padx=2, pady=2)
            ToolTip(plot, "Show the last saved plot")











    def upload(self):
        self.filename = filedialog.askopenfilename(
            title="Open plot configuration", 
            filetypes=[("JSON Files", "*.json")]
        )
        if not self.filename:
            return
        
        # Se non c'è un subplot attivo (es. app appena aperta), ne creiamo uno
        def to_stringvar(d, parent_key=None):
            if isinstance(d, dict):
                # Proteggiamo le CHIAVI del dizionario: k deve restare stringa
                return {k: to_stringvar(v, parent_key=k) for k, v in d.items()}
            
            elif isinstance(d, list):
                # Se la lista contiene ID, non trasformare i suoi elementi in StringVar
                keys_containing_ids = ["data_id", "inset_id", "function_id", "subplot_ids", "data", "inset", "function"]
                if parent_key in keys_containing_ids:
                    return d # Ritorna la lista di stringhe pure
                return [to_stringvar(x, parent_key=parent_key) for x in d]
            
            elif isinstance(d, str):
                # Campi critici che devono restare stringhe per non rompere i puntatori
                keys_to_keep_plain = ["subplot_id", "data_id", "inset_id", "function_id", "file path"]
                if parent_key in keys_to_keep_plain:
                    return d
                
                # Tutto il resto diventa StringVar (per la GUI)
                return tk.StringVar(value=d)
            
            else:
                return d

        #try:
        with open(self.filename, "r") as f:
            saved_data = json.load(f)

        # 1. Carica i dati nelle variabili di istanza (puntatori correnti)
        self.general_options["structure"]   = to_stringvar(saved_data.get("general_opt", {}))
        self.general_options["font"]        = to_stringvar(saved_data.get("font_opt", {}))
        self.default_options   = to_stringvar(saved_data.get("default_opt", {}))
        self.subplot_states    = to_stringvar(saved_data.get("subplots", {}))
        self.subplot_id = saved_data.get("subplot_ids", [])

        # 3. REFRESH GUI: Ricostruisce i widget grafici basandosi sui nuovi dati
        #self._refresh_workspace_gui()
        
        messagebox.showinfo("Successo", "Configurazione caricata nel subplot corrente.")

#        except Exception as e:
#            messagebox.showerror("Errore", f"Impossibile caricare la configurazione:\n{e}")
       
       
       
       
       
       
       
       
       
       
       
       
       
    def back_to_main(self):
        # Clear the existing content in the root window
        self.main_frame.destroy()
        self.menu_bar_frame.destroy()
        self.menu_frame.destroy()
        self.subplot_frame.destroy()
        self.dataplotter.setup_ui()
        
class MenuToggleManager:
    def __init__(self, main_page, general_options, default_options):
        self.main_page = main_page
        self.general_options = general_options
        self.default_options = default_options

        # Associazione ai due frame dedicati nei quali mostrerai i contenuti menu
        self.frame = main_page.menu_frame 
        self.content_frame = main_page.menu_content_frame      # per le opzioni base
        self.default_frame = main_page.menu_default_frame      # per le opzioni di default
        self.current_menu = None
        self.current_frame = None  # Tiene traccia del frame attualmente visibile

        # Mappa dei menu: nome -> funzione per costruire i widget
        self.menu_actions = {
            "file": self._file_menu,
            "opzioni_gen": lambda: GeneralOptions().options(self.content_frame, general_options['structure']),
            "aggiungi_subplot": lambda: LegendOptions().options(self.content_frame, general_options['legend']),
            "opzioni_font": lambda: FontOptions().options(self.content_frame, general_options['font']),
            "default": lambda: main_page.default_buttons(self.content_frame),
            "latex_convert": lambda: LatexConvert().convertion(self.content_frame),
            "constant": lambda: Constant().convertion(self.content_frame),

            "plot": lambda: DefaultPlot().options(self.default_frame, default_options['plot']),
            "hist": lambda: DefaultHist().options(self.default_frame, default_options['hist']),
            "scatter": lambda: DefaultScatter().options(self.default_frame, default_options['scatter']),
            "bar": lambda: DefaultBar().options(self.default_frame, default_options['bar']),
            "pie": lambda: DefaultPie().options(self.default_frame, default_options['pie']),
            "boxplot": lambda: DefaultBoxPlot().options(self.default_frame, default_options['boxplot']),
            "violin": lambda: DefaultViolin().options(self.default_frame, default_options['violin']),
            "heatmap": lambda: DefaultHeatmap().options(self.default_frame, default_options['heatmap']),
            "contour": lambda: DefaultContour().options(self.default_frame, default_options['contour']),
            "quiver": lambda: DefaultQuiver().options(self.default_frame, default_options['quiver']),
            "polar": lambda: DefaultPolar().options(self.default_frame, default_options['polar']),
            "stack": lambda: DefaultStack().options(self.default_frame, default_options['stack']),
        }

    def toggle(self, key):
        # Chiudi se stesso se già aperto
        if self.current_menu == key:
            self._hide_current()
            self.current_menu = None
            return

        # Chiudi quello attuale
        self._hide_current()

        # Decidi quale frame usare (content_frame o default_frame)
        if key in ["file", "opzioni_gen", "opzioni_font", "default", "latex_convert", "constant"]:
            frame = self.content_frame
        else:
            frame = self.default_frame
        self.current_frame = frame

        self.clear_menu_content(frame)

        # Mostra i nuovi widget nel frame giusto
        if key in self.menu_actions:
            self.menu_actions[key]()
            frame.grid()  # mostra il frame su cui stai lavorando
            self.frame.grid()
            self.current_menu = key
        else:
            print(f"Tasto {key} premuto (nessuna azione collegata)")

    def _hide_current(self):
        # Nascondi il frame attualmente aperto
        if self.current_frame is not None:
            self.current_frame.grid_remove()
            self.frame.grid_remove()  # Nascondi anche il frame principale

    def clear_menu_content(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _file_menu(self):
        LABEL_FONT = ("Arial", 10)
        self.clear_menu_content(self.content_frame)
        tk.Button(
            self.content_frame, text="Exit", command=self.main_page.quit, font=LABEL_FONT
        ).grid(row=0, column=0, sticky="ew", padx=10, pady=2)
        tk.Button(
            self.content_frame, text="Back to Menu", command=self.main_page.back_to_main, font=LABEL_FONT
        ).grid(row=0, column=1, sticky="ew", padx=10, pady=2)
