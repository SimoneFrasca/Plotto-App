import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, filedialog
from ui_elements import calcola, calcola_cost
from ui_elements import convert_file_to_csv, Functions, DATALOAD
from matplotlib.colors import to_rgba
import os
import json
import subprocess
import sys
from matplotlib.ticker import MaxNLocator

loader = DATALOAD()

class CreatePlot:
    def __init__(self, root, subplot_states, subplot_id, active_subplot_id, general_opt, default_opt, data_opt, 
                 inset_options, function_options, data_id, inset_id, function_id, save, show):
        
        self.root = root
        self.subplot_states = subplot_states 
        self.subplot_id = subplot_id
        self.active_subplot_id = active_subplot_id
        
        # Opzioni UI
        self.general_opt = general_opt
        self.font_opt = general_opt['font']
        self.structure_opt = general_opt['structure']
        self.default_opt = default_opt
                
        self.data_opt = data_opt
        self.inset_options = inset_options
        self.function_options = function_options
        self.data_id = data_id
        self.inset_id = inset_id
        self.function_id = function_id
        
        self.extreme = {'min': 0, 'max': 1}
        
        self.save = save
        self.show = show
        self.canvas = None
        self.fig = None
        
        self.create_figure()

    def check_positive(self, valore, nome_campo):
        if valore is None:
            return False
        else:
            if valore <= 0:
                messagebox.showerror("Errore Input", 
                    f"Il campo '{nome_campo}' è negativo.\n"
                    f"Valore inserito non valido: '{valore}'")
                return True
            else: 
                False
        
    def _get_val(self, container, key, cast_type=str, default=None):
        """Estrae i valori dalle variabili Tkinter gestendo errori e campi vuoti."""
        try:
            val = container[key].get()
            if val == "" or val is None:
                return default
            return cast_type(val)
        except (AttributeError, KeyError, ValueError):
            return default

    def get_and_validate(self, container, key, cast_type, nome_campo, default=1):
        # 1. Recupero il valore e pulizia base
        raw_val = str(container[key].get()).strip().replace(',', '.')

        # 2. Gestione campo vuoto
        if raw_val == "":
            return default

        try:
            # 3. Logica di Cast Dinamica
            if cast_type is int:
                # Se l'utente vuole un intero ma inserisce un punto decimale
                if "." in raw_val:
                    raise ValueError("Formato intero non valido (contiene decimali)")
                valore_final = int(raw_val)
                
            elif cast_type is float:
                valore_final = float(raw_val)
                
            else:
                # Se passi un altro tipo (es. str o un cast personalizzato)
                valore_final = cast_type(raw_val)

            return valore_final

        except ValueError:
            # Messaggio di errore personalizzato in base al tipo richiesto
            tipo_descr = "Intero" if cast_type is int else "Numerico"
            messagebox.showerror("Errore Input", 
                f"Il campo '{nome_campo}' richiede un valore di tipo [{tipo_descr}].\n"
                f"Valore inserito non valido: '{raw_val}'")
            return "ERRORE"

    def _setup_rc_params(self):
        """Configura lo stile globale di Matplotlib (Font, LaTeX, Colori, Dimensioni)."""
        
        # 1. Recupero valori (Cast sicuro ai tipi corretti)
        # Nota: Assumo che self.font_opt sia il nome corretto del dizionario
        is_tex = self._get_val(self.font_opt, "tex") == "Yes"
        color = self._get_val(self.font_opt, "color", str, "black")
        main_font = self._get_val(self.font_opt, "main_font", str, "sans-serif")
        
        # Recupero dimensioni
        title_size = self._get_val(self.font_opt, "title_size", float, 12.0)
        axis_label_size = self._get_val(self.font_opt, "label_size", float, 10.0)
        xtick_size = self._get_val(self.font_opt, "xaxis_size", float, 10.0)
        ytick_size = self._get_val(self.font_opt, "yaxis_size", float, 10.0)

        # 2. Configurazione Dizionario rc_params
        rc_params = {
            # --- Colori ---
            "text.color": color,
            "axes.labelcolor": color,
            "xtick.color": color,
            "ytick.color": color,
            "axes.titlecolor": color,
            # --- Dimensioni ---
            "axes.titlesize": title_size,      # Dimensione del Titolo del grafico
            "xtick.labelsize": xtick_size,     # Dimensione numeri asse X
            "ytick.labelsize": ytick_size,     # Dimensione numeri asse Y
            # Nota: Matplotlib ha un solo parametro globale 'axes.labelsize' per le label X e Y.
            # Uso 'xlabel_size' come default generale. Se vuoi Y diverso, va fatto nel plot specifico.
            "axes.labelsize": axis_label_size,
            # --- Font e LaTeX ---
            "text.usetex": is_tex,
            "font.family": main_font           # Imposta il font sia per TeX che standard
        }
        
        # 3. Gestione specifica per LaTeX
        if is_tex:
            # Se usi LaTeX, è fondamentale gestire il preambolo per i colori
            # E spesso conviene forzare il font serif/sans-serif se il nome del font specifico non è supportato da TeX
            rc_params["text.latex.preamble"] = r"\usepackage{xcolor}"
            
            # Opzionale: Se il main_font è un font di sistema specifico (es. "Arial"), 
            # LaTeX potrebbe dare errore. Spesso si usa:
            # rc_params["font.family"] = "serif" 
            
        # 4. Aggiornamento globale
        plt.rcParams.update(rc_params)

    def create_figure(self):
        # Cleanup preventiva
        if self.canvas: self.canvas.get_tk_widget().destroy()
        if self.fig: plt.close(self.fig)

        self._setup_rc_params()

        # Configurazione Griglia
        #rows = self._get_val(self.structure_opt, "row_plot", int, 1)
        
        rows = self.get_and_validate(container=self.structure_opt, key="row_plot", cast_type=int, nome_campo="Righe della Griglia",default=1)
        if rows == "ERRORE" or self.check_positive(rows,"Righe della Griglia"):
            return
        cols = self.get_and_validate(container=self.structure_opt, key="col_plot", cast_type=int, nome_campo="Colonne della Griglia",default=1)
        if cols == "ERRORE" or self.check_positive(cols,"Colonne della Griglia"):
            return
        
        fig_x = self.get_and_validate(container=self.structure_opt, key="x_dim", cast_type=float, nome_campo="Dimensione asse x",default=1)
        if fig_x == "ERRORE" or self.check_positive(fig_x,"Dimensione asse x"):
            return
        fig_y = self.get_and_validate(container=self.structure_opt, key="y_dim", cast_type=float, nome_campo="Dimensione asse y",default=1)
        if fig_y == "ERRORE" or self.check_positive(fig_y,"Dimensione asse y"):
            return
        
        print("dim, box:", fig_x, fig_y, rows, cols)
        self.fig, axes = plt.subplots(rows, cols, figsize=(fig_x, fig_y), squeeze=False)
        
        # Sfondo Figura
        self.fig.set_facecolor(self._get_val(self.structure_opt, "color", str, "white"))
        self.fig.patch.set_alpha(self._get_val(self.structure_opt, "alpha", float))
        
        if self._get_val(self.structure_opt, "title"):
            self.fig.suptitle(self._get_val(self.structure_opt, "title"))

        if rows * cols == 1:
            sid = self.active_subplot_id
            subplot = self.subplot_states[sid]
            print("stiamo stampando il subplot:", sid)
            
            ax = axes[0,0]
            # Gestione Dati e Inset
            self.data_opt = subplot["data_options"]
            self.inset_options = subplot["inset_options"]
            self.function_options = subplot["function_options"]
            # ID elementi
            self.data_id = subplot["data_id"]
            self.inset_id = subplot["inset_id"]
            self.function_id = subplot["function_id"]
            self.sid = sid
            self._plot_contents(ax, subplot)

        else:
            for i, (sid, subplot) in enumerate(self.subplot_states.items()):
                if i >= rows * cols:
                    print(f"Warning: Griglia insufficiente per {sid}")
                    break
                
                print("stiamo stampando il subplot:", sid)
                
                sub_row = self.get_and_validate(container=subplot['structure'], key="row", cast_type=int, nome_campo=f"posizione riga di {sid}",default=None)
                if sub_row == "ERRORE" or self.check_positive(sub_row,f"posizione riga di {sid}"):
                    return
            
                sub_col = self.get_and_validate(container=subplot['structure'], key="col", cast_type=int, nome_campo=f"posizione colonna di {sid}",default=None)
                if sub_col == "ERRORE" or self.check_positive(sub_col,f"posizione colonna di {sid}"):
                    return
            
                print("row col: ", sub_row,sub_col)
                
                if sub_row is not None and sub_col is not None:    
                    if sub_row >= rows or sub_col >= cols:
                        messagebox.showwarning(
                            "Attenzione", 
                            f"La posizione impostata per '{sid}' [{sub_row}, {sub_col}] "
                            f"eccede la griglia totale {rows}x{cols}."
                            f"Ricorda che la prima posizione ha indici [0,0]"
                        )
                        return
                    ax = axes[sub_row, sub_col]
                else:
                    ax = axes[i // cols, i % cols]
                        
                # Gestione Dati e Inset
                self.data_opt = subplot["data_options"]
                self.inset_options = subplot["inset_options"]
                self.function_options = subplot["function_options"]
                # ID elementi
                self.data_id = subplot["data_id"]
                self.inset_id = subplot["inset_id"]
                self.function_id = subplot["function_id"]
                self.sid = sid
                self._plot_contents(ax, subplot)
            
        self.fig.tight_layout()

        if self.save:
            self.save_path = filedialog.asksaveasfilename(
                title="Save plot as image",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf"), ("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")]
            )
            if self.save_path:
                save_path_without_ext, _ = os.path.splitext(self.save_path)
                plt.savefig(self.save_path)
                self.save_config_and_data(save_path_without_ext + "_config.json")
                print(f"\nPlot saved as {self.save_path}")

        else:
            print("\nPlot not saved. Configuration saved on the Desktop as plot_configuration.json")
            self.save_config_and_data("plot_configuration.json")
            
        if self.show:
            plt.show()
        else:
            self._render_to_tkinter()

    def _plot_contents(self, ax, subplot):
        for inset_id in self.inset_id:
            if inset_id != "inset_0" and self.inset_options[inset_id]["show/hide"].get() == "0":
                print(f"{inset_id} non plottato")
            else:
                target_ax = ax
                if inset_id == "inset_0":
                    self.configure_axes(ax, subplot['structure'])
                else: 
                    target_ax = self.create_inset(ax, inset_id)
                
                # Qui chiameresti le tue funzioni di disegno originali
                if hasattr(self, 'plot_data_for_inset'):
                    self.plot_data_for_inset(target_ax, inset_id)
                if hasattr(self, 'plot_functions_for_inset'):
                    self.plot_functions_for_inset(target_ax, inset_id)
                
                if inset_id == "inset_0":
                    self._apply_legend(ax, subplot['legend'])
                else:
                    legend_opts = self.inset_options[inset_id]["legend"]
                    if self._get_val(legend_opts, 'legend') == "Yes":
                        legend_args = {
                            # Posizionamento e Stile Base
                            'loc': self._get_val(legend_opts, 'legend_position', str, 'best'),
                            'fontsize': self._get_val(legend_opts, 'legend_size', float, 10),
                        }
                        target_ax.legend(**legend_args)

    def _setup_rc_params_inset(self, ax, opts):
        """Configura lo stile di un singolo asse (inset) manualmente."""
        
        # 1. Recupero valori
        # Nota: text.usetex è globale, è difficile cambiarlo solo per un ax. 
        # Qui lo ignoriamo o assumiamo segua il globale, ma possiamo cambiare il font.
        color = self._get_val(opts, "color", str, "black")
        main_font = self._get_val(self.font_opt, "main_font", str, "sans-serif")
        title_size = self._get_val(opts, "title_size", float, 12.0)
        axis_label_size = self._get_val(opts, "label_size", float, 10.0)
        xtick_size = self._get_val(opts, "xaxis_size", float, 10.0)
        ytick_size = self._get_val(opts, "yaxis_size", float, 10.0)

        # 2. Applicazione diretta all'oggetto ax
        
        # --- Colori e Dimensioni dei Tick (le tacchette e i numeri) ---
        ax.tick_params(axis='x', colors=color, labelsize=xtick_size)
        ax.tick_params(axis='y', colors=color, labelsize=ytick_size)
        
        # --- Colore del bordo del grafico (Spines) ---
        for spine in ax.spines.values():
            spine.set_edgecolor(color)

        # --- Configurazione Label Asse X ---
        xaxis_label = ax.xaxis.get_label()
        xaxis_label.set_color(color)
        xaxis_label.set_size(axis_label_size)
        xaxis_label.set_family(main_font)

        # --- Configurazione Label Asse Y ---
        yaxis_label = ax.yaxis.get_label()
        yaxis_label.set_color(color)
        yaxis_label.set_size(axis_label_size)
        yaxis_label.set_family(main_font)

        # --- Configurazione Titolo ---
        title = ax.title
        title.set_color(color)
        title.set_size(title_size)
        title.set_family(main_font)

        # --- Aggiornamento Font dei numeri sugli assi (Tick Labels) ---
        # Questo è necessario perché tick_params cambia size/color ma non il font family
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontfamily(main_font)
     
    def create_inset(self, ax, inset_id):
        opts = self.inset_options[inset_id]
        target_ax = ax.inset_axes([
            float(opts['position']["left"].get()),
            float(opts['position']["bottom"].get()),
            float(opts['position']["width"].get()),
            float(opts['position']["height"].get())
        ])
        self._setup_rc_params_inset(target_ax,opts["font"])
        self.configure_axes(target_ax, opts)
        return target_ax
    
    def configure_axes(self, ax, opts):                
        ax.set_facecolor(self._get_val(opts, "facecolor", str))
        ax.patch.set_alpha(self._get_val(opts, "alpha_face", float))

        ax.spines['top'].set_visible(True if self._get_val(opts["spines"], "top", int) == 1 else False) # Rimuove bordo superiore
        ax.spines['right'].set_visible(True if self._get_val(opts["spines"], "right", int) == 1 else False) # Rimuove bordo destro
        ax.spines['left'].set_visible(True if self._get_val(opts["spines"], "left", int) == 1 else False) # Rimuove bordo sinistro
        ax.spines['bottom'].set_visible(True if self._get_val(opts["spines"], "bottom", int) == 1 else False) # Rimuove bordo inferiore

        """Configura un singolo asse (principale o inset)."""
        # Label e Titoli
        ax.set_title(self._get_val(opts, "title", str, ""))
        ax.set_xlabel(self._get_val(opts, "x_label", str, ""))
        ax.set_ylabel(self._get_val(opts, "y_label", str, ""))

        # Limiti (applica solo se entrambi definiti)
        x_min = self.get_and_validate(opts, "x_min", float, f"x min di {self.sid}", None)
        if x_min == "ERRORE":
            return
        x_max = self.get_and_validate(opts, "x_max", float, f"x max di {self.sid}", None)
        if x_max == "ERRORE":
            return
        
        y_min = self.get_and_validate(opts, "y_min", float, f"y min di {self.sid}", None)
        if x_min == "ERRORE":
            return
        y_max = self.get_and_validate(opts, "y_max", float, f"y max di {self.sid}", None)
        if x_max == "ERRORE":
            return
        
        if x_min is not None and x_max is not None: 
            if x_min > x_max:
                messagebox.showerror("Errore Input", f"x min > x_max in {self.sid}\n")
                return
            else:
                ax.set_xlim(x_min, x_max)
        if y_min is not None and y_max is not None: 
            if y_min > y_max:
                messagebox.showerror("Errore Input", f"x min > x_max in {self.sid}\n")
                return
            else:
                ax.set_ylim(y_min, y_max)
        
        # Gestione ticks
        x_thick = self.get_and_validate(container=opts, key="x_thick", cast_type=int, nome_campo=f"x thick di {self.sid}",default=None)
        if x_thick == "ERRORE" or self.check_positive(x_thick,f"x thick di {self.sid}"):
            return
        y_thick = self.get_and_validate(container=opts, key="y_thick", cast_type=int, nome_campo=f"y thick di {self.sid}",default=None)
        if y_thick == "ERRORE" or self.check_positive(x_thick,f"y thick di {self.sid}"):
            return
        if x_thick is not None:
            ax.xaxis.set_major_locator(MaxNLocator(nbins=x_thick))
        if y_thick is not None:
            ax.yaxis.set_major_locator(MaxNLocator(nbins=y_thick))
            
        # Formattazione Scientifica
        sci = opts['sci']
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        min_sci = self.get_and_validate(sci, "min_scilimits", int, f"min scilimits di {self.sid}",0)
        if min_sci == "Erorre":
            return
        max_sci = self.get_and_validate(sci, "max_scilimits", int, f"min scilimits di {self.sid}",0)
        if max_sci == "Erorre":
            return
        ax.ticklabel_format(
            style=self._get_val(sci, 'style', str, 'plain'),
            axis=self._get_val(sci, 'axis', str, 'both'),
            scilimits=(min_sci,max_sci)
        )

        # Scale Logaritmiche
        log_type = self._get_val(opts, "log", str, "Linear")
        if "Log" in log_type:
            if "x" in log_type or "Log Log" in log_type: ax.set_xscale('log')
            if "y" in log_type or "Log Log" in log_type: ax.set_yscale('log')

        # Griglia
        grid = opts['grid']
        if self._get_val(grid, 'style') != "None":
            ax.grid(True, 
                    linestyle=self._get_val(grid, 'style', str, '-'),
                    lw=self._get_val(grid, 'lw', float, 0.5),
                    color=self._get_val(grid, 'color', str, 'gray'),
                    alpha=self._get_val(grid, 'alpha', float, 0.3),
                    axis=self._get_val(grid, 'axis', str, 'both'))
          
    def _apply_legend(self, ax, l_opt):
        """Applica la legenda con tutti i parametri di rifinitura avanzati."""
        
        # 1. Verifica se l'utente vuole visualizzare la legenda
        if self._get_val(l_opt, 'legend') != "Yes":
            # Se c'è una legenda preesistente, la rimuoviamo, altrimenti usciamo
            if ax.get_legend():
                ax.get_legend().remove()
            return

        # 2. Configurazione Dizionario argomenti Matplotlib
        legend_args = {
            # Posizionamento e Stile Base
            'loc': self._get_val(l_opt, 'legend_position', str, 'best'),
            'fontsize': self._get_val(l_opt, 'legend_size', float, 10),
            'title': self._get_val(l_opt, 'legend_title', str, ""),
            'frameon': self._get_val(l_opt, 'legend_frame') == "Yes",
            'framealpha': self._get_val(l_opt, 'legend_alpha', float, 1.0),
            'shadow': self._get_val(l_opt, 'legend_shadow') == "Yes",
            'ncol': self._get_val(l_opt, 'legend_ncol', int, 1),
            
            # Spaziature e Dimensioni (Parametri di rifinitura)
            'borderpad': self._get_val(l_opt, 'legend_borderpad', float, 0.4),      # Spazio dentro il bordo
            'labelspacing': self._get_val(l_opt, 'legend_labelspacing', float, 0.5), # Spazio verticale tra voci
            'handlelength': self._get_val(l_opt, 'legend_handlelength', float, 2.0), # Lunghezza linea/simbolo
            'handleheight': self._get_val(l_opt, 'legend_handleheight', float, 0.7), # Altezza dell'area del simbolo
            'handletextpad': self._get_val(l_opt, 'legend_handletextpad', float, 0.8), # Spazio tra simbolo e testo
            'borderaxespad': self._get_val(l_opt, 'legend_borderaxespad', float, 0.5), # Spazio tra legenda e assi
            'markerscale': self._get_val(l_opt, 'legend_markerscale', float, 1.0)      # Scala dei simboli nella legenda
        }

        # Pulizia: Se il titolo è vuoto, è meglio rimuovere la chiave o passare None
        # (Matplotlib gestisce "", ma in alcuni casi None è più pulito)
        if not legend_args['title']:
            legend_args['title'] = None

        # 3. Applicazione
        ax.legend(**legend_args)

    def _render_to_tkinter(self):
        """Incolla il grafico nell'interfaccia Tkinter."""
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(self.fig)

    def save_config_and_data(self, filename):
        """Salva l'intera configurazione e lo stato di tutti i subplot in un file JSON."""
        
        def serialize(obj):
            """Converte ricorsivamente variabili Tkinter e strutture dati."""
            # 1. Gestione variabili Tkinter (StringVar, IntVar, ecc.)
            # Verifichiamo che abbia .get e NON sia un dizionario
            if hasattr(obj, "get") and callable(obj.get) and not isinstance(obj, dict):
                return obj.get()       
            # 2. Gestione Dizionari
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            # 3. Gestione Liste o Set
            if isinstance(obj, (list, set)):
                return [serialize(i) for i in obj]
            # 4. Gestione tipi primitivi
            if isinstance(obj, (int, float, str, bool, type(None))):
                return obj
            
            # Fallback
            return str(obj)

        # Il resto della funzione rimane invariato...
        data_to_save = {
            "general_opt": serialize(self.structure_opt),
            "default_opt": serialize(self.default_opt),
            "font_opt": serialize(self.font_opt),
            "subplots": {
                sid: {
                    "subplot_id": sid,
                    "structure": serialize(state.get("structure")),
                    "legend": serialize(state.get("legend")),
                    "inset_frame_visible": serialize(state.get("inset_frame_visible")),
                    "data_id": serialize(state.get("data_id")),
                    "inset_id": serialize(state.get("inset_id")),
                    "function_id": serialize(state.get("function_id")),
                    "data_options": serialize(state.get("data_options")),
                    "inset_options": serialize(state.get("inset_options")),
                    "function_options": serialize(state.get("function_options")),
                    "columns": serialize(state.get("columns")),
                    "data_counter": serialize(state.get("data_counter")),
                    "function_counter": serialize(state.get("function_counter")),
                    "inset_counter": serialize(state.get("inset_counter"))
                } for sid, state in self.subplot_states.items()
            },
            "subplot_ids": serialize(self.subplot_id),
        }

        try:
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")

    def show_saved_file(self, path):
        """Apre il file salvato con l'applicazione predefinita del sistema."""
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
            
    # ----- Plot dei dati -----
    def plot_data_for_inset(self, ax, inset_id):
        ids = [d for d in self.data_id if inset_id in d]
        for data_id in ids:
            options = self.data_opt[data_id]
            if options['show/hide'].get() == "0":
                print(f"{data_id} non plottato")
            else:
                if options['plot_select'].get() == "plot":
                    self.plot(options, ax)
                elif options['plot_select'].get() == "hist":
                    self.hist(options, ax)
                elif options['plot_select'].get() == "scatter":
                    self.scatter(options, ax)
                elif options['plot_select'].get() == "bar":
                    self.bar(options, ax)
                elif options['plot_select'].get() == "pie":
                    self.pie(options, ax)
                elif options['plot_select'].get() == "boxplot":
                    self.boxplot(options, ax)
                elif options['plot_select'].get() == "violin":
                    self.violin(options, ax)
                elif options['plot_select'].get() == "heatmap":
                    self.heatmap(options, ax)
                elif options['plot_select'].get() == "contour":
                    self.contour(options, ax)
                elif options['plot_select'].get() == "quiver":
                    self.quiver(options, ax)
                elif options['plot_select'].get() == "polar":
                    self.polar(options, ax)
                elif options['plot_select'].get() == "stack":
                    self.stack(options, ax)

    def plot_functions_for_inset(self, ax, inset_id):
        ids = [f for f in self.function_id if inset_id in f]
        for function_id in ids:
            fun = self.function_options[function_id]
            if fun['show/hide'].get() == "0":
                print(f"{function_id} non plottato")
            else:
                if fun["function_select"].get() == "function":
                    self.plot_function(fun["function"], ax)
                if fun["function_select"].get() == "h-line":
                    self.plot_axhline(fun["axhline"], ax)
                if fun["function_select"].get() == "v-line":
                    self.plot_axvline(fun["axvline"], ax)
                if fun["function_select"].get() == "h-span":
                    self.plot_axhspan(fun["axhspan"], ax)
                if fun["function_select"].get() == "v-span":
                    self.plot_axvspan(fun["axvspan"], ax)
                if fun["function_select"].get() == "patch":
                    self.plot_patch(fun["patch"], ax)

    # ----- Funzioni di utilità -----
    def safe_float(self, value):
        return float(value) if value else None

    def update_extreme(self, datax):
        self.extreme['min'] = min(self.extreme['min'], min(datax))
        self.extreme['max'] = max(self.extreme['max'], max(datax))

    def fit(self, datax, options, ax):
        x = np.linspace(np.min(datax), np.max(datax), 1000)
        reg_type = options['fit']['type'].get()
        popt = options['fit']['params']
        opt = options['fit']

        if reg_type == "Linear":
            y = Functions.linear(x, *popt)
        elif reg_type == "Quadratic":
            y = Functions.quadratic(x, *popt)
        elif reg_type == "Polynomial":
            y = np.poly1d(popt)(x)
        elif reg_type == "Logarithmic":
            mask = x > 0
            x = x[mask]
            y = Functions.logarithmic(x, *popt)
        elif reg_type == "Exponential":
            y = Functions.exponential(x, *popt)
        elif reg_type == "Power law":
            mask = x > 0
            x = x[mask]
            y = Functions.powerlaw(x, *popt)
        elif reg_type == "Sigmoid":
            y = Functions.sigmoid(x, *popt)
        elif reg_type == "Gaussian":
            y = Functions.gaussian(x, *popt)
        elif reg_type == "Lorentzian":
            y = Functions.lorentzian(x, *popt)
        elif reg_type == "Voigt":
            y = Functions.voigt(x, *popt)
        elif reg_type == "Lognormal":
            y = Functions.lognormal(x, *popt)
        elif reg_type == "Exponential PDF":
            y = Functions.exponential_pdf(x, *popt)
        elif reg_type == "Skewed Gaussian":
            y = Functions.skewed_gaussian(x, *popt)
            

        ax.plot(
            x, y,
            linestyle=opt['line'].get() if opt['line'].get() != "None" else self.plot_opt['def_line'].get(),
            linewidth=float(opt['lw'].get()) if opt['lw'].get() != "" else float(self.plot_opt['def_lw'].get()),
            color=opt['color'].get() if opt['color'].get() != "" else self.plot_opt['def_color'].get(),
            alpha=float(opt['alpha'].get()) if opt['alpha'].get() != "" else 1.0,
            label=opt['label'].get() if opt['label'].get() != "" else None
        )

    # ----- Plot semplice -----
    def plot(self, options, ax):
        common = options['common']
        plot_opt = options['plot']
        error_opt = options['plot']['errorbar']
        def_plot_opt = self.default_opt['plot']
        def_errorbar_opt = self.default_opt['plot']['errorbar']
        x_col, y_col = common['x'].get(), plot_opt['y'].get()
        x2_col, y2_col = common['x2'].get(), plot_opt['y2'].get()
        
        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        x_min = self.get_and_validate(common, "x_min", float, f"x min di {options['data_id']}", None)
        if x_min == "ERRORE":
            return
        x_max = self.get_and_validate(common, "x_max", float, f"x max di {options['data_id']}", None)
        if x_max == "ERRORE":
            return
        if (x_min is not None and x_max is not None) and x_min > x_max:
            messagebox.showerror("Errore Input", f"x min > x max in {options['data_id']}\n")
            return
    
        y_min = self.get_and_validate(plot_opt, "y_min", float, f"y min di {options['data_id']}", None)
        if x_min == "ERRORE":
            return
        y_max = self.get_and_validate(plot_opt, "y_max", float, f"y max di {options['data_id']}", None)
        if x_max == "ERRORE":
            return        
        if (y_min is not None and y_max is not None) and y_min > y_max:
            messagebox.showerror("Errore Input", f"y min > ymax in {options['data_id']}\n")
            return
        
        
        col_filter1 = common['col_filter1'].get()
        filter1 = common['filter1'].get()
        col_compare_filter1 = common['col_compare_filter1'].get()
        col_filter2 = common['col_filter2'].get()
        filter2 = common['filter2'].get()
        col_compare_filter2 = common['col_compare_filter2'].get()
        col_filter3 = common['col_filter3'].get()
        filter3 = common['filter3'].get()
        col_compare_filter3 = common['col_compare_filter3'].get()
        col_filter4 = common['col_filter4'].get()
        filter4 = common['filter4'].get()
        col_compare_filter4 = common['col_compare_filter4'].get()


        datax, datay, xerr, yerr = loader.read(
            file_path=options['file path'], 
            x=x_col, y=y_col, xerr=common['x_err'].get(), yerr=plot_opt['y_err'].get(),
            x2=x2_col, y2=y2_col,
            x_min=x_min,x_max=x_max,y_min=y_min,y_max=y_max,
            filters1={"cat": col_filter1,"val": filter1,"compare": col_compare_filter1},
            filters2={"cat": col_filter2,"val": filter2,"compare": col_compare_filter2},
            filters3={"cat": col_filter3,"val": filter3,"compare": col_compare_filter3},
            filters4={"cat": col_filter4,"val": filter4,"compare": col_compare_filter4}, 
            x_fun = common['x_function'].get(), x_par = common['x_parameters'].get(),
            y_fun = common['y_function'].get(), y_par = common['y_parameters'].get(),
        )
        if datax is None or datay is None:
            return

        self.update_extreme(datax)

        try:

            # Parametri comuni per plot/errorbar
            plot_args = {
                'color': common['color'].get(),
                'alpha': float(common['alpha'].get()),
                'linestyle': def_plot_opt['def_line'].get() if def_plot_opt['def_line'].get() != "None" else plot_opt['line'].get(),
                'marker': def_plot_opt['def_marker'].get() if def_plot_opt['def_marker'].get() != "None" else plot_opt['marker'].get(),
                'markersize': float(plot_opt['ms'].get()) if def_plot_opt['def_ms'].get() == "" else float(def_plot_opt['def_ms'].get()),
                'linewidth': float(plot_opt['lw'].get()) if def_plot_opt['def_lw'].get() == "" else float(def_plot_opt['def_lw'].get()),
                'markerfacecolor': plot_opt['mfcolor'].get() if plot_opt["mfc"].get() == "Yes" else common['color'].get(),
                'label': common['label'].get()
            }

            print(options['inset'],common['label'].get())
            # Usa errorbar solo se almeno uno tra xerr e yerr è definito
            if xerr is not None or yerr is not None:
                # Colore errorbar
                plot_args['ecolor'] = (def_errorbar_opt['ecolor'].get() if def_errorbar_opt['ecolor'].get() != "None"else error_opt["ecolor"].get())
                # Spessore linea delle barre
                plot_args['elinewidth'] = (float(def_errorbar_opt['elinewidth'].get()) if def_errorbar_opt['elinewidth'].get() != "" else float(error_opt["elinewidth"].get()))
                # Lunghezza cappette
                plot_args['capsize'] = (float(def_errorbar_opt['capsize'].get())if def_errorbar_opt['capsize'].get() != "" else float(error_opt["capsize"].get()))
                # Spessore cappette
                plot_args['capthick'] = (float(def_errorbar_opt['capthick'].get()) if def_errorbar_opt['capthick'].get() != "" else float(error_opt["capthick"].get()))
                plot_args['xerr'] = xerr
                plot_args['yerr'] = yerr
                ax.errorbar(datax,datay,**plot_args)
            else:
                ax.plot(datax,datay,**plot_args)
            
            if options['fit']['plot_reg'].get() == "Yes":
                self.fit(datax, options, ax)
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while plotting: {e}")
            return

    # ----- Istogramma -----
    def hist(self, options, ax):
        common = options['common']
        hist_opt = options['hist']
        tick_par = hist_opt['tick_par']
        
        x = common['x'].get()
        if x == "None":
            messagebox.showerror("Error", "X data not selected.")
            return
        x2_col = common['x2'].get()
        
        x_min = self.get_and_validate(common, "x_min", float, f"x min di {options['data_id']}", None)
        if x_min == "ERRORE":
            return
        x_max = self.get_and_validate(common, "x_max", float, f"x max di {options['data_id']}", None)
        if x_max == "ERRORE":
            return
        if (x_min is not None and x_max is not None) and x_min > x_max:
            messagebox.showerror("Errore Input", f"x min > x max in {options['data_id']}\n")
            return
        
        col_filter1 = common['col_filter1'].get()
        filter1 = common['filter1'].get()
        col_compare_filter1 = common['col_compare_filter1'].get()
        col_filter2 = common['col_filter2'].get()
        filter2 = common['filter2'].get()
        col_compare_filter2 = common['col_compare_filter2'].get()
        col_filter3 = common['col_filter3'].get()
        filter3 = common['filter3'].get()
        col_compare_filter3 = common['col_compare_filter3'].get()
        col_filter4 = common['col_filter4'].get()
        filter4 = common['filter4'].get()
        col_compare_filter4 = common['col_compare_filter4'].get()


        datax, _, _, _ = loader.read(
            file_path=options['file path'], 
            x=x, y=None, xerr=None, yerr=None,
            x2=x2_col, y2=None,
            x_min=x_min,x_max=x_max,y_min=None,y_max=None,
            filters1={"cat": col_filter1,"val": filter1,"compare": col_compare_filter1},
            filters2={"cat": col_filter2,"val": filter2,"compare": col_compare_filter2},
            filters3={"cat": col_filter3,"val": filter3,"compare": col_compare_filter3},
            filters4={"cat": col_filter4,"val": filter4,"compare": col_compare_filter4}, 
            x_fun = common['x_function'].get(), x_par = common['x_parameters'].get(),
            y_fun = None, y_par = None,
        )
        if datax is None:
            return

        self.update_extreme(datax)
        
        # preparo i valori
        """facecolor = (
            self.structure_opt['def_color'].get()
            if self.structure_opt['def_color'].get() != "None"
            else common['color'].get()
        )
        face_alpha = (
            float(self.structure_opt['alpha'].get())
            if self.structure_opt['def_color'].get() != "None"
            else float(common['alpha'].get())
        )
        edgecolor = (
            self.structure_opt['def_color'].get()
            if self.structure_opt['def_color'].get() != "None"
            else hist_opt['contour_color'].get()
        )
        contour_alpha = (
            float(self.structure_opt['alpha'].get())
            if self.structure_opt['def_color'].get() != "None"
            else float(hist_opt['contour_alpha'].get())
        )
"""
        histtype = hist_opt['histtype'].get()
        facecolor = common['color'].get()
        face_alpha = float(common['alpha'].get())
        edgecolor = hist_opt['contour_color'].get()
        contour_alpha = float(hist_opt['contour_alpha'].get())
        face_rgba = to_rgba(facecolor, face_alpha) if facecolor != "None" else "none"
        edge_rgba = to_rgba(edgecolor, contour_alpha)

        # dizionario di argomenti validi per ax.hist
        hist_args = {
            'histtype': histtype,
            'bins': int(hist_opt['bins'].get()),
            'density': True if hist_opt['density'].get() == "True" else False,
            'align': hist_opt['align'].get(),
            'orientation': hist_opt['orientation'].get(),
            'cumulative': True if hist_opt['cumulative'].get() == "True" else False,
            'bottom': float(hist_opt['bottom'].get()),
            'rwidth': float(hist_opt['rwidth'].get()),
            'facecolor': face_rgba,
            'edgecolor': edge_rgba,
            'linewidth': hist_opt['contour_width'].get(),
            'linestyle': hist_opt['contour_line'].get(),
            'label': common['label'].get()
        }
        
        clean_params = {
            'axis':       tick_par['axis'].get(),
            'direction':  tick_par['direction'].get(),
            'length':     float(tick_par['length'].get()),    # Converti in numero
            'width':      float(tick_par['width'].get()),     # Converti in numero
            'color':      tick_par['color'].get(),
            'labelcolor': tick_par['labelcolor'].get(),
            'labelsize':  float(tick_par['labelsize'].get()), # Converti in numero
            'pad':        float(tick_par['pad'].get())        # Converti in numero
        }
        
        # 2. Applichiamo i parametri all'asse desiderato
        ax.tick_params(**clean_params)

        # disegno istogramma
        ax.hist(datax, **hist_args)
        
        if options['fit']['plot_reg'].get() == "Yes":
            self.fit(datax, options, ax)

    # ----- Scatter Plot -----
    def scatter(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['scatter']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, xerr, yerr = loader.read(
            options['file path'], 
            x_col, y_col, 
            common['x_err'].get(), options['scatter']['y_err'].get()
        )
        self.update_extreme(datax)

        ax.scatter(datax, datay,
                   color=options['scatter']['color'].get() or self.plot_opt['def_color'].get(),
                   alpha=float(options['scatter']['alpha'].get() or 0.5),
                   edgecolor=options['scatter']['edge_color'].get() or 'black',
                   s=float(options['scatter']['size'].get() or 20))
        
    # ----- Bar Chart -----
    def bar(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['bar']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        ax.bar(datax, datay,
               color=options['bar']['color'].get() or self.plot_opt['def_color'].get(),
               width=float(options['bar']['width'].get() or 0.8))
    
    # ----- Pie Chart -----
    def pie(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['pie']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        ax.pie(datay, labels=datax,
               autopct=options['pie']['autopct'].get() or '%1.1f%%',
               startangle=float(options['pie']['startangle'].get() or 90),
               colors=options['pie']['colors'].get().split(',') or None)
        
    # ----- Boxplot -----
    def boxplot(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['boxplot']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        ax.boxplot(datay, vert=bool(options['boxplot']['vert'].get()),
                   patch_artist=bool(options['boxplot']['patch_artist'].get()))
    
    # ----- Violin Plot -----
    def violin(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['violin']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        ax.violinplot(datay, showmeans=bool(options['violin']['showmeans'].get()),
                      showextrema=bool(options['violin']['showextrema'].get()))
    
    # ----- Heatmap -----
    def heatmap(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['heatmap']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        # Crea una matrice 2D per la heatmap
        heatmap_data = np.array(datay).reshape(-1, 1)
        cax = ax.imshow(heatmap_data, cmap=options['heatmap']['cmap'].get() or 'viridis',
                        interpolation=options['heatmap']['interpolation'].get() or 'nearest')
        ax.figure.colorbar(cax, ax=ax)
        
    # ----- Contour Plot -----
    def contour(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['contour']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        # Crea una griglia per il contour plot
        X, Y = np.meshgrid(datax, datay)
        Z = np.sin(X) * np.cos(Y)
    
        contours = ax.contour(X, Y, Z, levels=10, cmap=options['contour']['cmap'].get() or 'viridis')
        ax.clabel(contours, inline=True, fontsize=8)
    
    # ----- Quiver Plot -----
    def quiver(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['quiver']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, y_col, 
            None, None
        )
        self.update_extreme(datax)

        # Crea una griglia per il quiver plot
        X, Y = np.meshgrid(datax, datay)
        U, V = -Y, X
        ax.quiver(X, Y, U, V,
                  color=options['quiver']['color'].get() or self.plot_opt['def_color'].get(),
                  scale=float(options['quiver']['scale'].get() or 1),
                  angles=options['quiver']['angles'].get() or 'xy')

    # ----- Polar Plot -----
    def polar(self, options, ax):
        common = options['common']
        theta_col, r_col = common['x'].get(), options['polar']['y'].get()

        if theta_col == "None" or r_col == "None":
            messagebox.showerror("Error", "Theta or R data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            theta_col, r_col, 
            None, None
        )
        self.update_extreme(datax)

        ax.set_theta_zero_location('N')
        ax.plot(datax, datay,
                color=options['polar']['color'].get() or self.plot_opt['def_color'].get(),
                linewidth=float(options['polar']['lw'].get() or 1))
        
    # ----- Stack Plot -----
    def stack(self, options, ax):
        common = options['common']
        x_col = common['x'].get()

        if x_col == "None":
            messagebox.showerror("Error", "X data not selected.")
            return

        datax, datay, _, _ = loader.read(
            options['file path'], 
            x_col, None, 
            None, None
        )
        self.update_extreme(datax)

        # Supponiamo che datay sia una lista di liste per lo stackplot
        ax.stackplot(datax, *datay,
                     labels=options['stack']['labels'].get().split(',') or None,
                     colors=options['stack']['colors'].get().split(',') or None)
        ax.legend(loc=options['stack']['legend'].get() or 'upper left')
        
    
    # ----- Funzione -----
    def plot_function(self, options, ax): 
        expr = options['function'].get().strip()
        parameters = options['parameters'].get().strip()
        if not expr: return
        xmin = float(options['x min'].get() or self.extreme['min'])
        xmax = float(options['x max'].get() or self.extreme['max'])
        X = np.linspace(xmin, xmax, 1000)
        #try:
        Y = calcola(X, None, expr, parameters)
        if Y is None:
            print(f"⚠️ Errore: la funzione '{expr}' con parametri '{parameters}' non ha prodotto un risultato valido.")
            return

        if not isinstance(Y, np.ndarray):
            try:
                Y = np.array(Y, dtype=float)
            except Exception as e:
                print(f"⚠️ Errore di conversione in array: {e}")
                return

        ax.plot(X, Y,
                color=options['color'].get() or None,
                label=options['label'].get() or None,
                linestyle=options['line'].get() or self.plot_opt['def_line'].get(),
                linewidth=float(options['lw'].get() or self.plot_opt['def_lw'].get() or 1)
            )
        
     # ----- Funzione -----
    
    # ----- axhline -----
    def plot_axhline(self, options, ax):
        y = calcola_cost(options["y"].get())
        label = options["label"].get()
        line = options["line"].get()
        lw = options["lw"].get()
        color = options["color"].get()
        alpha = float(options["alpha"].get())
        
        ax.axhline(y=y,label=label if label != "" else None,linestyle=line,linewidth=lw,color=color,alpha=alpha,)

    def plot_axvline(self, options, ax):
        x = calcola_cost(options["x"].get())
        label = options["label"].get()
        line = options["line"].get()
        lw = options["lw"].get()
        color = options["color"].get()
        alpha = float(options["alpha"].get())
        
        ax.axvline(x=x,label=label if label != "" else None,linestyle=line,linewidth=lw,color=color,alpha=alpha)

    # ----- axhspan -----
    def plot_axhspan(self, options, ax):
        y1 = calcola_cost(options["y1"].get())
        y2 = calcola_cost(options["y2"].get())
        label = options["label"].get()
        facecolor = options["facecolor"].get()
        edgecolor = options["edgecolor"].get()
        alpha = float(options["alpha"].get())
        
        ax.axhspan(y1, y2, facecolor=facecolor,edgecolor=edgecolor, alpha=alpha,label=label)

    # ----- axvspan -----
    def plot_axvspan(self, options, ax):
        x1 = calcola_cost(options["x1"].get())
        x2 = calcola_cost(options["x2"].get())
        label = options["label"].get()
        facecolor = options["facecolor"].get()
        edgecolor = options["edgecolor"].get()
        alpha = float(options["alpha"].get())
        
        ax.axvspan(x1, x2, facecolor=facecolor,edgecolor=edgecolor, alpha=alpha,label=label)
        
    # ----- Patch -----
    def plot_patch(self, options, ax):
        x1 = calcola_cost(options["x1"].get())
        x2 = calcola_cost(options["x2"].get())
        y1 = calcola_cost(options["y1"].get())
        y2 = calcola_cost(options["y2"].get())
        label = options["label"].get()
        line = options["line"].get()
        lw = float(options["lw"].get())
        facecolor = options["facecolor"].get()
        edgecolor = options["edgecolor"].get()
        alpha = float(options["alpha"].get())
        
        width = x2 - x1
        height = y2 - y1

        rect = patches.Rectangle(
            (x1, y1),
            width,
            height,
            linewidth=lw,
            linestyle=line,
            facecolor=facecolor,
            edgecolor=edgecolor,
            alpha=alpha,
            label=label if label != "" else None,
        )

        ax.add_patch(rect)
            
    