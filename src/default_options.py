import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from ui_elements import dim, MARKER, LINE, LOG, YN , TF, LEGEND, FONTS, HISTTYPE, ORIENTATION, ALIGN, Helper, AXIS, COLOR, ToolTip
import re

ui = Helper

class GeneralOptions:
    def __init__(self):
        # Only default values, no frame
        self.general_opt = {
            'x_dim': tk.StringVar(value="4"), 
            'y_dim': tk.StringVar(value="3"), 
            'row_plot': tk.StringVar(value="1"),
            'col_plot': tk.StringVar(value="1"),            
            'title': tk.StringVar(value=None),
            'color': tk.StringVar(value="None"),
            'alpha': tk.StringVar(value="1"),
            'adjust_aspect': tk.StringVar(value="No"),
        }
        
    def options(self, root, general_opt, upload=False):
        self.general_opt.update(general_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=0)
        
        if upload:
            self.general_opt = general_opt
        
        row = 0; col = 0
        _, col = ui.add_label_entry(frame, "Title:", self.general_opt['title'], entry_width=50, row=row, col=col, tooltip="Titolo principale del grafico")
        _, col = ui.add_label_entry(frame, "X dimension:", self.general_opt['x_dim'], entry_width=8, row=row, col=col, tooltip="Largezza grafico")
        _, col = ui.add_label_entry(frame, "Y dimension:", self.general_opt['y_dim'], entry_width=8, row=row, col=col, tooltip="Altezza grafico")
        _, col = ui.add_label_entry(frame, "row-col plots", self.general_opt['row_plot'], entry_width=4, row=row, col=col, tooltip="Numero di righe/colonne subplot")
        _, col = ui.add_label_entry(frame, "-", self.general_opt['col_plot'], entry_width=4, row=row, col=col, tooltip="Numero di righe/colonne subplot")
        _, col = ui.add_color(frame, self.general_opt['color'], row=row, col=col, tooltip="Colore sfondo")
        _, col = ui.add_scale(frame, self.general_opt['alpha'], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparenza sfondo")
        
        general_opt.update(self.general_opt)
        
class SubplotOptions:
    def __init__(self):
        # Only default values, no frame
        self.general_opt = {
            'row': tk.StringVar(value=None),
            'col': tk.StringVar(value=None),
            'title': tk.StringVar(value=None),
            'x_label': tk.StringVar(value=None), 
            'y_label': tk.StringVar(value=None),
            'x_min': tk.StringVar(value=None), 
            'x_max': tk.StringVar(value=None),
            'y_min': tk.StringVar(value=None), 
            'y_max': tk.StringVar(value=None),
            'x_thick': tk.StringVar(value=None),
            'y_thick': tk.StringVar(value=None),
            'log': tk.StringVar(value='None'),
            'def_color': tk.StringVar(value="None"),
            'def_alpha': tk.StringVar(value=""),
            
            'facecolor': tk.StringVar(value="None"),
            'alpha_face': tk.StringVar(value="1"),
            
            'spines': {
                'left': tk.StringVar(value="1"),
                'top': tk.StringVar(value="1"),
                'right': tk.StringVar(value="1"),
                'bottom': tk.StringVar(value="1"),
            },
            
            'grid': {
                'style': tk.StringVar(value='None'),
                'lw': tk.StringVar(value=0.5),
                'color': tk.StringVar(value=COLOR[5]),
                'alpha': tk.StringVar(value=0.5),
                'axis': tk.StringVar(value='both'),
            },
            'sci': {
                'style': tk.StringVar(value='plain'),
                'axis': tk.StringVar(value='both'),
                'min_scilimits': tk.StringVar(value=0),
                'max_scilimits': tk.StringVar(value=0)
            },
        }
        
    def options(self, root, general_opt, upload=False):
        self.general_opt.update(general_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=0)
        
        if upload:
            self.general_opt = general_opt
        
        _, col = ui.add_label_entry(frame, "Position:", self.general_opt['row'], entry_width=5, row=0, col=0, tooltip="Riga della sottotrama (Subplot Row)")
        _, col = ui.add_label_entry(frame, "-", self.general_opt['col'], entry_width=5, row=0, col=2, tooltip="Colonna della sottotrama (Subplot Column)")
        _, col = ui.add_label_optionmenu(frame, "Logarithmic:", self.general_opt['log'], LOG, row=0, col=4, tooltip="Imposta la scala logaritmica per gli assi", colorbg=None) # colorbg non definito qui nel tuo originale
        
        _, col = ui.add_label_entry(frame, "Title:", self.general_opt['title'], entry_width=80, row=1, col=0, columnspan=6, tooltip="Titolo del grafico")
        
        color = "lightblue"
        body_frame = tk.Frame(frame , bg =color, borderwidth=1, relief=tk.SUNKEN)
        body_frame.grid(row=0, column=7, rowspan=3)
        row = 0; col = 0
        _, col = ui.add_color(body_frame, self.general_opt["facecolor"], row=row, col=col, tooltip="Colore di sfondo dell'area del grafico")
        _, col = ui.add_scale(body_frame, self.general_opt['alpha_face'], from_=0, to=1, resolution=0.05, row=row, col=col, tooltip="Opacità dello sfondo del grafico", colorbg=color)
        
        spine_frame = tk.Frame(body_frame, bg="lightblue", borderwidth=1, relief=tk.SUNKEN)
        spine_frame.grid(row=1, column=0,columnspan=2)
        _, _ = ui.add_label(spine_frame, "┌────", row=0, col=0, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "TOP", self.general_opt["spines"]["top"], row=0, col=1, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo superiore", colorbg=color)
        _, _ = ui.add_label(spine_frame, "────┐", row=0, col=2, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "LEFT", self.general_opt["spines"]["left"], row=1, col=0, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo sinistro", colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "RIGHT", self.general_opt["spines"]["right"], row=1, col=2, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo destro", colorbg=color)
        _, _ = ui.add_label(spine_frame, "└────", row=2, col=0, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "BOTTOM", self.general_opt["spines"]["bottom"], row=2, col=1, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo inferiore", colorbg=color)
        _, _ = ui.add_label(spine_frame, "────┘", row=2, col=2, label_font=dim.label_font(12), colorbg=color)
        
        color = "lightgreen"
        grid_frame = tk.Frame(frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        grid_frame.grid(row=0, column=8, rowspan=3)
        _, col = ui.add_label_optionmenu(grid_frame, "Grid:", self.general_opt["grid"]["axis"], AXIS, row=0, col=0, tooltip="Seleziona su quali assi visualizzare la griglia", colorbg=color)
        _, col = ui.add_optionmenu(grid_frame, self.general_opt['grid']['style'], LINE, row=1, col=0, tooltip="Stile della linea della griglia", colorbg=color)
        _, col = ui.add_scale(grid_frame, self.general_opt["grid"]['lw'], from_=0, to=3, resolution=0.1, row=1, col=1, tooltip="Spessore della linea della griglia", colorbg=color)
        _, col = ui.add_color(grid_frame, self.general_opt["grid"]["color"], row=2, col=0, tooltip="Colore delle linee della griglia")
        _, col = ui.add_scale(grid_frame, self.general_opt["grid"]['alpha'], from_=0, to=1, resolution=0.05, row=2, col=1, tooltip="Trasparenza della griglia", colorbg=color)
        
        color = "lightblue"
        sci_frame = tk.Frame(frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        sci_frame.grid(row=0, column=9, rowspan=3)
        _, col = ui.add_label(sci_frame, "Scientific notation:", row=0, col=0, colspan=3, tooltip="Scegli tra formato decimale standard o scientifico", colorbg=color)
        _, col = ui.add_optionmenu(sci_frame, self.general_opt['sci']['style'], ['plain', 'sci'], row=1, col=0, colspan=3, tooltip="Stile:\n⦿ Plain: standard (es. 1000)\n⦿ Sci: scientifico (es. 1e3)", colorbg=color)
        _, col = ui.add_optionmenu(sci_frame, self.general_opt['sci']['axis'], AXIS, row=2, col=0, colspan=3, tooltip="Asse su cui applicare la notazione", colorbg=color)
        _, col = ui.add_entry(sci_frame, self.general_opt['sci']['min_scilimits'], entry_width=8, row=3, col=0, tooltip="Limite inferiore per notazione scientifica\n(Es: n → attiva per valori < 10^n)")
        _, col = ui.add_label_entry(sci_frame, "-", self.general_opt['sci']['max_scilimits'], entry_width=8, row=3, col=1, tooltip="Limite superiore per notazione scientifica\n(Es: m → attiva per valori ≥ 10^m)", colorbg=color)
        
        color = "lightgreen"
        axis_frame = tk.Frame(frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        axis_frame.grid(row=2, column=0, columnspan=6)
        row = 0; col = 0
        _, col = ui.add_label_entry(axis_frame, "X axis:", self.general_opt['x_label'], entry_width=40, row=row, col=col, tooltip="Etichetta asse X", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "min/max:", self.general_opt['x_min'], entry_width=8, row=row, col=col, tooltip="Limite minimo asse X", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "-", self.general_opt['x_max'], entry_width=8, row=row, col=col, tooltip="Limite massimo asse X", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "thick", self.general_opt['x_thick'], entry_width=8, row=row, col=col, tooltip="Numero o spaziatura delle tacche (ticks) asse X", colorbg=color)
        row = 1; col = 0
        _, col = ui.add_label_entry(axis_frame, "Y axis:", self.general_opt['y_label'], entry_width=40, row=row, col=col, tooltip="Etichetta asse Y", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "min/max:", self.general_opt['y_min'], entry_width=8, row=row, col=col, tooltip="Limite minimo asse Y", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "-", self.general_opt['y_max'], entry_width=8, row=row, col=col, tooltip="Limite massimo asse Y", colorbg=color)
        _, col = ui.add_label_entry(axis_frame, "thick", self.general_opt['y_thick'], entry_width=8, row=row, col=col, tooltip="Numero o spaziatura delle tacche (ticks) asse Y", colorbg=color)
        
        general_opt.update(self.general_opt)

class LegendOptions:
    def __init__(self, legend_opt=None):
        self.legend = {
            'legend': tk.StringVar(value="No"),
            'legend_position': tk.StringVar(value=LEGEND[0]),
            'legend_size': tk.StringVar(value="10"),
            'legend_title': tk.StringVar(value=""),
            'legend_frame': tk.StringVar(value="Yes"),
            'legend_alpha': tk.StringVar(value="1.0"),
            'legend_shadow': tk.StringVar(value="No"),
            'legend_borderpad': tk.StringVar(value="0.4"),
            'legend_labelspacing': tk.StringVar(value="0.5"),
            'legend_handlelength': tk.StringVar(value="2.0"),
            'legend_handleheight': tk.StringVar(value="0.7"),
            'legend_handletextpad': tk.StringVar(value="0.8"),
            'legend_borderaxespad': tk.StringVar(value="0.5"),
            'legend_ncol': tk.StringVar(value="1"),
            'legend_markerscale': tk.StringVar(value="1.0")
        }

        if legend_opt:
            for key, value in legend_opt.items():
                if key in self.legend:
                    self.legend[key].set(value)

    def options(self, root, legend_opt):
        self.legend.update(legend_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=0, column=0, padx=5, pady=5)

        # --- RIGA 0: Aspetto Generale e Visibilità ---
        row = 0; col = 0
        _, col = ui.add_label_optionmenu(frame, "Show Legend:", self.legend['legend'], YN, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Show Frame:", self.legend['legend_frame'], YN, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Shadow:", self.legend['legend_shadow'], YN, row=row, col=col)
        _, col = ui.add_label(frame, "Transparency:", row=row, col=col)
        _, col = ui.add_scale(frame, self.legend['legend_alpha'], from_=0, to=1, resolution=0.05, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Position:", self.legend['legend_position'], LEGEND, row=row, col=col)

        # --- RIGA 1: Posizione, Titolo e Font ---
        row = 1; col = 0
        _, col = ui.add_label_entry(frame, "Size:", self.legend['legend_size'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Title:", self.legend['legend_title'], entry_width=35, row=row, col=col, columnspan=3)
        col += 2 # Spazio per il columnspan
        _, col = ui.add_label(frame, "Columns (ncol):", row=row, col=col)
        _, col = ui.add_spinbox(frame, self.legend['legend_ncol'], from_=1, to=10, increment=1, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Border Pad:", self.legend['legend_borderpad'], entry_width=8, row=row, col=col)

        # --- RIGA 2: Dimensioni e Padding (Dettagli tecnici) ---
        row = 2; col = 0
        _, col = ui.add_label_entry(frame, "Label Spacing:", self.legend['legend_labelspacing'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Marker Scale:", self.legend['legend_markerscale'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Handle Length:", self.legend['legend_handlelength'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Handle Text Pad:", self.legend['legend_handletextpad'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Handle Height:", self.legend['legend_handleheight'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Border Axes Pad:", self.legend['legend_borderaxespad'], entry_width=8, row=row, col=col)

        legend_opt.update(self.legend)

class FontOptions:
    def __init__(self):
        self.font_options = {
            "main_font": tk.StringVar(value=FONTS[0]),      # Font principale (default generale)
            "tex": tk.StringVar(value="No"),                # Usare LaTeX per i testi
            "title_size": tk.StringVar(value="10"),         # Dimensione titolo
            "label_size": tk.StringVar(value="10"),         # Dimensione label assi
            "xaxis_size": tk.StringVar(value="10"),        # Dimensione label asse X
            "yaxis_size": tk.StringVar(value="10"),        # Dimensione label asse Y
            "color": tk.StringVar(value=COLOR[5])            # Colore dei testi
        }

    def options(self, root, font_opt):
        self.font_options.update(font_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)
    
        row = 1
        col = 0
        _, col = ui.add_label_optionmenu(frame, "Font:", self.font_options["main_font"], FONTS, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Title Size:", self.font_options["title_size"], entry_width=8,row=row, col=col)
        _, col = ui.add_label_entry(frame, "Label Size:", self.font_options["label_size"], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "X axis size:", self.font_options["xaxis_size"], entry_width=8, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Y axis size:", self.font_options["yaxis_size"], entry_width=8, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Tex:", self.font_options["tex"], YN, row=row, col=col)
        _, col = ui.add_color(frame, self.font_options["color"], row=row, col=col, tooltip="Color")

        font_opt.update(self.font_options)
  
class LatexConvert:
    def __init__(self):
        self.textvariable = tk.StringVar()
        self.result_var = tk.StringVar()  # mostra l'espressione convertita

    def convertion(self, root):
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        row, col = 0, 0
        # Messaggio di istruzioni
        _, col = ui.add_label(frame, "Use LaTeX syntax to write mathematical expressions.\nExamples: $\\alpha$, $\\beta^2$, $\\int_a^b f(x)dx$, etc.",
                              row=row, col=col, label_font=dim.label_font(15))
        _, col = ui.add_label(frame, "Expression:", row=row, col=col)
        _, col = ui.add_text(frame, self.textvariable, width = 120, row=row, col=col)
        _, col = ui.add_label(frame, " -- Convertion -->", row=row, col=col)
        result_label = tk.Label(frame, textvariable=self.result_var, fg="blue", justify="left")
        result_label.grid(row=row, column=col, sticky="w", pady=5)

        # Pulsante copia 📋
        copy_button = tk.Button(frame, text="📋", command=lambda: self.copy_to_clipboard(root))
        copy_button.grid(row=row, column=col+2, sticky="w", padx=5)

        ToolTip(copy_button, "Copy")  # usa la tua versione elegante

        # Associa aggiornamento automatico al cambio di testo
        self.textvariable.trace_add("write", lambda *args: self.update_result())

    def update_result(self):
        expr_input = self.textvariable.get()
        expr_converted = self.convert(expr_input)
        self.result_var.set(expr_converted)

    def copy_to_clipboard(self, root):
        """Copia il testo convertito negli appunti"""
        root.clipboard_clear()
        root.clipboard_append(self.result_var.get())
        root.update()  # per mantenere il contenuto negli appunti

    def convert(self, expr):
        expr = expr.replace(" ", "")

        # --- Funzioni trigonometriche ---
        expr = expr.replace(r"\sin", "np.sin")
        expr = expr.replace(r"\cos", "np.cos")
        expr = expr.replace(r"\tan", "np.tan")

        # --- Inverse trig ---
        expr = expr.replace(r"\arcsin", "np.arcsin")
        expr = expr.replace(r"\arccos", "np.arccos")
        expr = expr.replace(r"\arctan", "np.arctan")

        # --- Esponenziale ---
        expr = expr.replace(r"\exp", "np.exp")
        expr = re.sub(r"e\^({?)(.*?)(}?)", r"np.exp(\2)", expr)  # es. e^x → np.exp(x)

        # --- Radici quadrate ---
        expr = re.sub(r"\\sqrt\{([^}]*)\}", r"np.sqrt(\1)", expr)   # \sqrt{x+y} → np.sqrt(x+y)
        expr = re.sub(r"\\sqrt\(([^)]*)\)", r"np.sqrt(\1)", expr)   # \sqrt(x) → np.sqrt(x)

        # --- Potenze ---
        expr = re.sub(r"(\w+)\^({?)(.*?)(}?)", r"\1**\3", expr)  # x^2 → x**2

        # --- Logaritmi ---
        expr = expr.replace(r"\ln", "np.log")      # log naturale
        expr = expr.replace(r"\log", "np.log10")   # log base 10

        # --- Frazioni ---
        expr = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"(\1)/(\2)", expr)  
        # es. \frac{1}{x+1} → (1)/(x+1)

        # --- Integrali ---
        expr = re.sub(r"\\int_([^{^}]*)\^([^{^}]*)", r"integrate(\1,\2,", expr)
        # es. \int_0^1 f(x)dx → integrate(0,1,f(x))

        # --- Sommatorie ---
        expr = re.sub(r"\\sum_{([^}]*)}\^{([^}]*)}", r"sum_over(\1,\2,", expr)
        # es. \sum_{n=1}^{10} n^2 → sum_over(n=1,10,n**2)

        # --- Prodotti ---
        expr = re.sub(r"\\prod_{([^}]*)}\^{([^}]*)}", r"prod_over(\1,\2,", expr)
        # es. \prod_{k=1}^{n} k → prod_over(k=1,n,k)

        return expr
    

class Constant:
    def __init__(self):
        self.textvariable = tk.StringVar()
        self.result_var = tk.StringVar()  # mostra l'espressione convertita

    def constant(self, root):
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        row, col = 0, 0
        # Pi greco
        _, col = ui.add_label(frame, "Pi (π):", row, col, padx=5, pady=5, sticky="w", tooltip="Rapporto circonferenza/diametro")
        _, col = ui.add_copy_text(frame, "3.1415926535", row, col, padx=5, pady=5, sticky="w", tooltip=None)
        
        # Numero di Nepero
        _, col = ui.add_label(frame, "e (Nepero):", row, col, padx=5, pady=5, sticky="w", tooltip="Base dei logaritmi naturali")
        _, col = ui.add_copy_text(frame, "2.7182818284", row, col, padx=5, pady=5, sticky="w", tooltip=None)
        
        # Sezione Aurea
        _, col = ui.add_label(frame, "Phi (φ):", row, col, padx=5, pady=5, sticky="w", tooltip="Sezione Aurea")
        _, col = ui.add_copy_text(frame, "1.6180339887", row, col, padx=5, pady=5, sticky="w", tooltip=None)
        
        # Radice di 2
        _, col = ui.add_label(frame, "sqrt(2):", row, col, padx=5, pady=5, sticky="w", tooltip="Costante di Pitagora")
        _, col = ui.add_copy_text(frame, "1.4142135623", row, col, padx=5, pady=5, sticky="w", tooltip=None)
        
        # Costante di Eulero-Mascheroni
        _, col = ui.add_label(frame, "Gamma (γ):", row, col, padx=5, pady=5, sticky="w", tooltip="Costante di Eulero-Mascheroni")
        _, col = ui.add_copy_text(frame, "0.5772156649", row, col, padx=5, pady=5, sticky="w", tooltip=None)
        
#-----------------------------------------------------------------------------------------------------------------------------------

class DefaultPlot:
    def __init__(self):
        
        self.default_plot = {
            'def_marker': tk.StringVar(value="None"),
            'def_ms': tk.StringVar(value=""),
            'def_line': tk.StringVar(value="None"),
            'def_lw': tk.StringVar(value=""),
            'def_mfc': tk.StringVar(value="Yes"),
            "errorbar": {
                "ecolor": tk.StringVar(value="None"),
                "elinewidth": tk.StringVar(value=""),
                "capsize": tk.StringVar(value=""),
                "capthick": tk.StringVar(value="")
            }
        }

    def options(self, root, plot_opt):
        self.default_plot.update(plot_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Data Options", row=0, col=0, colspan=7, label_font=dim.label_font(12))

        row = 1
        col = 0
        _, col = ui.add_label_optionmenu(frame, "Marker Style:", self.default_plot["def_marker"], MARKER, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Marker size:", self.default_plot["def_ms"], row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Line Style:", self.default_plot["def_line"], LINE, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Line width:", self.default_plot["def_lw"], row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "MFC:", self.default_plot["def_mfc"], YN, row=row, col=col)
        
        plot_opt.update(self.default_plot)
        
class DefaultHist:
    def __init__(self):
        
        self.hist = {
            'def_density': tk.StringVar(value="False"),
            'def_bins': tk.StringVar(value=""),
            'def_weights': tk.StringVar(value=None),
            'def_cumulative': tk.StringVar(value="False"), 
            'def_bottom': tk.StringVar(value=None), 
            'def_histtype': tk.StringVar(value=HISTTYPE[0]), 
            'def_align': tk.StringVar(value=ALIGN[0]), 
            'def_orientation': tk.StringVar(value=ORIENTATION[0]), 
            'def_rwidth': tk.StringVar(value=None),
            'def_stacked': tk.StringVar(value="False")
        }
        
    def options(self, root, hist_opt):
        self.hist.update(hist_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        row = 1
        col = 0

        _, col = ui.add_label_optionmenu(frame, "Hist type:", self.hist['def_histtype'], HISTTYPE, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Align:", self.hist['def_align'], ALIGN, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Orientation:", self.hist['def_orientation'], ORIENTATION, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Stacked:", self.hist['def_stacked'], TF, row=row, col=col)

        row += 1
        col = 0
        _, col = ui.add_label_optionmenu(frame, "Density:", self.hist['def_density'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Cumulative:", self.hist['def_cumulative'], TF, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Bins:", self.hist['def_bins'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Bottom:", self.hist['def_bottom'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Weights:", self.hist['def_weights'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Rwidth:", self.hist['def_rwidth'], row=row, col=col)
     
        hist_opt.update(self.hist)
        
class DefaultScatter:
    def __init__(self):
        self.scatter = {
            'def_marker': tk.StringVar(value="o"),       # marker shape
            'def_ms': tk.StringVar(value=""),            # marker size
            'def_cmap': tk.StringVar(value="viridis"),   # colormap (per colorazione da array)
            'def_alpha': tk.StringVar(value=""),         # trasparenza
            'def_edgecolor': tk.StringVar(value=COLOR[0]),# bordo dei marker
            'def_linewidths': tk.StringVar(value=""),    # spessore bordo
        }

    def options(self, root, scatter_opt):
        self.scatter.update(scatter_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Scatter Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row = 1
        col = 0
        _, col = ui.add_label_optionmenu(frame, "Marker Style:", self.scatter['def_marker'], MARKER, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Marker size:", self.scatter['def_ms'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Alpha:", self.scatter['def_alpha'], row=row, col=col)
        
        row += 1
        col = 0
        _, col = ui.add_label_entry(frame, "Edge Color:", self.scatter['def_edgecolor'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Linewidths:", self.scatter['def_linewidths'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Colormap:", self.scatter['def_cmap'], row=row, col=col)

        scatter_opt.update(self.scatter)

class DefaultBar:
    def __init__(self):
        self.bar = {
            'def_width': tk.StringVar(value="0.8"),      # larghezza barre
            'def_align': tk.StringVar(value="center"),   # allineamento (center/edge)
            'def_alpha': tk.StringVar(value=""),         # trasparenza
            'def_color': tk.StringVar(value=COLOR[0]),     # colore barre
            'def_edgecolor': tk.StringVar(value=COLOR[5]) # colore bordo
        }

    def options(self, root, bar_opt):
        self.bar.update(bar_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Bar Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Width:", self.bar['def_width'], row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Align:", self.bar['def_align'], ALIGN, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Alpha:", self.bar['def_alpha'], row=row, col=col)

        row += 1
        col = 0
        _, col = ui.add_color(frame, self.bar['def_color'], row=row, col=col, tooltip="Color")
        _, col = ui.add_color(frame, self.bar['def_edgecolor'], row=row, col=col, tooltip="Color")

        bar_opt.update(self.bar)

class DefaultPie:
    def __init__(self):
        self.pie = {
            'def_autopct': tk.StringVar(value="%1.1f%%"), # formato percentuali
            'def_startangle': tk.StringVar(value="90"),   # angolo di partenza
            'def_shadow': tk.StringVar(value="No"),       # ombra
            'def_explode': tk.StringVar(value=None),      # separazione spicchi
        }

    def options(self, root, pie_opt):
        self.pie.update(pie_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Pie Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Autopct:", self.pie['def_autopct'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Start Angle:", self.pie['def_startangle'], row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Shadow:", self.pie['def_shadow'], YN, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Explode:", self.pie['def_explode'], row=row, col=col)

        pie_opt.update(self.pie)

class DefaultBoxPlot:
    def __init__(self):
        self.box = {
            'def_notch': tk.StringVar(value="False"),
            'def_vert': tk.StringVar(value="True"),
            'def_patch_artist': tk.StringVar(value="True"),
            'def_meanline': tk.StringVar(value="False"),
            'def_showmeans': tk.StringVar(value="False"),
        }

    def options(self, root, box_opt):
        self.box.update(box_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default BoxPlot Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_optionmenu(frame, "Notch:", self.box['def_notch'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Vertical:", self.box['def_vert'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Patch Artist:", self.box['def_patch_artist'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Mean Line:", self.box['def_meanline'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Show Means:", self.box['def_showmeans'], TF, row=row, col=col)

        box_opt.update(self.box)

class DefaultViolin:
    def __init__(self):
        self.violin = {
            'def_showmeans': tk.StringVar(value="False"),
            'def_showextrema': tk.StringVar(value="True"),
            'def_showmedians': tk.StringVar(value="False"),
            'def_vert': tk.StringVar(value="True"),
            'def_widths': tk.StringVar(value=None),
        }

    def options(self, root, violin_opt):
        self.violin.update(violin_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Violin Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_optionmenu(frame, "Show Means:", self.violin['def_showmeans'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Show Extrema:", self.violin['def_showextrema'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Show Medians:", self.violin['def_showmedians'], TF, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Vertical:", self.violin['def_vert'], TF, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Widths:", self.violin['def_widths'], row=row, col=col)

        violin_opt.update(self.violin)

class DefaultHeatmap:
    def __init__(self):
        self.heatmap = {
            'def_cmap': tk.StringVar(value="viridis"),
            'def_interpolation': tk.StringVar(value="nearest"),
            'def_aspect': tk.StringVar(value="auto"),
        }

    def options(self, root, heatmap_opt):
        self.heatmap.update(heatmap_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Heatmap Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Cmap:", self.heatmap['def_cmap'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Interpolation:", self.heatmap['def_interpolation'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Aspect:", self.heatmap['def_aspect'], row=row, col=col)

        heatmap_opt.update(self.heatmap)

class DefaultContour:
    def __init__(self):
        self.contour = {
            'def_levels': tk.StringVar(value="10"),
            'def_cmap': tk.StringVar(value="viridis"),
            'def_alpha': tk.StringVar(value=""),
        }

    def options(self, root, contour_opt):
        self.contour.update(contour_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Contour Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Levels:", self.contour['def_levels'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Cmap:", self.contour['def_cmap'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Alpha:", self.contour['def_alpha'], row=row, col=col)

        contour_opt.update(self.contour)

class DefaultQuiver:
    def __init__(self):
        self.quiver = {
            'def_scale': tk.StringVar(value=None),
            'def_width': tk.StringVar(value=None),
            'def_headwidth': tk.StringVar(value=None),
            'def_headlength': tk.StringVar(value=None),
            'def_headaxislength': tk.StringVar(value=None),
        }

    def options(self, root, quiver_opt):
        self.quiver.update(quiver_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Quiver Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Scale:", self.quiver['def_scale'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Width:", self.quiver['def_width'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Head Width:", self.quiver['def_headwidth'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Head Length:", self.quiver['def_headlength'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Head Axis Length:", self.quiver['def_headaxislength'], row=row, col=col)

        quiver_opt.update(self.quiver)

class DefaultPolar:
    def __init__(self):
        self.polar = {
            'def_marker': tk.StringVar(value="None"),
            'def_line': tk.StringVar(value="-"),
            'def_lw': tk.StringVar(value="1"),
            'def_color': tk.StringVar(value=COLOR[0]),
            'def_alpha': tk.StringVar(value=""),
        }

    def options(self, root, polar_opt):
        self.polar.update(polar_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Polar Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_optionmenu(frame, "Marker:", self.polar['def_marker'], MARKER, row=row, col=col)
        _, col = ui.add_label_optionmenu(frame, "Line:", self.polar['def_line'], LINE, row=row, col=col)
        _, col = ui.add_label_entry(frame, "Line width:", self.polar['def_lw'], row=row, col=col)

        row += 1
        col = 0
        _, col = ui.add_color(frame, self.polar['def_color'], row=row, col=col, tooltip="Color")
        _, col = ui.add_label_entry(frame, "Alpha:", self.polar['def_alpha'], row=row, col=col)

        polar_opt.update(self.polar)

class DefaultStack:
    def __init__(self):
        self.stack = {
            'def_labels': tk.StringVar(value=None),
            'def_alpha': tk.StringVar(value=""),
        }

    def options(self, root, stack_opt):
        self.stack.update(stack_opt)
        frame = tk.Frame(root, relief=tk.SUNKEN, borderwidth=3)
        frame.grid(row=2, column=1)

        ui.add_label(frame, "Default Stackplot Options", row=0, col=0, colspan=6, label_font=dim.label_font(12))

        row, col = 1, 0
        _, col = ui.add_label_entry(frame, "Labels:", self.stack['def_labels'], row=row, col=col)
        _, col = ui.add_label_entry(frame, "Alpha:", self.stack['def_alpha'], row=row, col=col)

        stack_opt.update(self.stack)
