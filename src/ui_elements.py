import tkinter as tk
import pandas as pd
import re
import csv
import tempfile
import numpy as np
from scipy.special import wofz, erf # Necessari per Voigt e Skewed Gaussian
from tkinter import messagebox

BASE_WIDTH = 3840
BASE_HEIGHT = 2160

MARKER = ["o", ",", ".", "v", "^", "<", ">", "s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_", "P", "X", "None"]
COLOR = ["blue", "green", "red", "magenta","orange", "black", "violet",
         "purple", "brown", "pink", "gray", "yellow", "olive", "teal",
         "indigo", "turquoise", "gold", "cyan", "silver", "beige", "white"]
LINE = ['solid', 'dashed', 'dashdot', 'dotted', 'None']
LOG = ['SemiLog x', 'SemiLog y', 'Log Log', 'None']
YN = ['Yes', 'No']
AXIS = ['x', 'y', 'both']
LEGEND = ['best','upper right','upper left','lower left','lower right','right',
          'center left','center right','lower center','upper center','center']
HISTTYPE = ['bar', 'barstacked', 'step', 'stepfilled']
ORIENTATION = ['vertical', 'horizontal']
ALIGN = ['left', 'mid', 'right']
LEGEND = ['best','upper left','upper center','upper right','center left','center','center right','lower left','lower center','lower right']
TF = ['True', 'False']
FONTS = [
            # Computer Modern (default LaTeX fonts)
            "Computer Modern Roman",         # serif
            "Computer Modern Sans Serif",   # sans-serif
            "Computer Modern Typewriter",   # monospaced

            # Latin Modern (miglioramenti di Computer Modern, molto usati in LaTeX)
            "Latin Modern Roman",           # serif
            "Latin Modern Sans",            # sans-serif
            "Latin Modern Mono",            # monospaced

            # Classici font LaTeX
            "Times",                        # spesso usato come Times-Roman in LaTeX
            "Helvetica",                    # sans-serif molto comune
            "Palatino",                     # serif elegante
            "Bookman",                      # serif
            "Avant Garde",                  # sans-serif moderno
            "Courier",                      # monospaced classico

            # Font LaTeX meno comuni ma compatibili
            "Utopia",                       # serif usato in alcune classi LaTeX
            "Charter",                      # serif leggibile, ben supportato
            "Nimbus Roman",                 # alternativa a Times
            "Nimbus Sans",                  # alternativa a Helvetica

            # DejaVu (default Matplotlib, compatibili con LaTeX + matplotlib.rc)
            "DejaVu Serif",
            "DejaVu Sans"
        ]
PLOT = ["plot", "hist", "scatter", "bar", "pie", "boxplot", "violin", "heatmap", "contour", "quiver", "polar", "stack"]
FUNCTION = ["function", "h-line", "v-line", "h-span", "v-span", "patch"]
REGRESSION_FUNCTIONS = [
    "Linear", 
    "Quadratic", 
    "Polynomial", 
    "Logarithmic", 
    "Exponential", 
    "Power law", 
    "Sigmoid", 
    "Gaussian", 
    "Lorentzian", 
    "Voigt", 
    "Lognormal", 
    "Exponential PDF", 
    "Skewed Gaussian"
]

LABEL_SIZE = 14
ENTRY_SIZE = 14

col_index = {color: i for i, color in enumerate(COLOR, start=1)}

def convert_file_to_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    processed_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        if i == 0:
            line = line.replace("# ", "")
            line = line.replace("#", "")
        fields = re.split(r'\s+', line)
        processed_lines.append(fields)

    # Salva il file temporaneo CSV
    temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', newline='', encoding='utf-8')
    writer = csv.writer(temp_csv)
    for row in processed_lines:
        writer.writerow(row)
    temp_csv.close()
    return temp_csv.name

class Functions:
    # ==========================================
    # --- FUNZIONI MATEMATICHE BASE ---
    # ==========================================

    @staticmethod
    def linear(x, a, b):
        """ y = ax + b """
        return a*x + b

    @staticmethod
    def quadratic(x, a, b, c):
        """ y = ax^2 + bx + c """
        return a*x**2 + b*x + c

    @staticmethod
    def polynomial(x, *coeffs):
        """ Polinomio di grado arbitrario: coeffs = [an, ..., a1, a0] """
        return np.poly1d(coeffs)(x)

    @staticmethod
    def logarithmic(x, a, b):
        """ y = a * ln(x) + b """
        return a * np.log(x) + b

    @staticmethod
    def exponential(x, a, b):
        """ y = a * e^(bx) (Crescita/Decrescita semplice) """
        return a * np.exp(b*x)

    @staticmethod
    def powerlaw(x, a, b):
        """ y = a * x^b """
        return a * np.power(x, b)

    @staticmethod
    def sigmoid(x, L, x0, k):
        """ Funzione sigmoide (logistica) """
        return L / (1 + np.exp(-k*(x-x0)))

    # ==========================================
    # --- DISTRIBUZIONI STATISTICHE (PER FIT ISTOGRAMMI) ---
    # ==========================================

    @staticmethod
    def gaussian(x, amp, mu, sigma):
        """
        Distribuzione Normale (Gaussiana).
        amp   : Ampiezza (altezza del picco)
        mu    : Media (posizione del centro)
        sigma : Deviazione standard (larghezza)
        """
        return amp * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

    @staticmethod
    def lorentzian(x, amp, x0, gamma):
        """
        Distribuzione di Cauchy-Lorentz (comune in spettroscopia).
        amp   : Ampiezza del picco
        x0    : Centro del picco
        gamma : HWHM (Half Width at Half Maximum), parametro di larghezza
        """
        return amp * (gamma**2 / ((x - x0)**2 + gamma**2))

    @staticmethod
    def voigt(x, amp, x0, sigma, gamma):
        """
        Profilo di Voigt (Convoluzione di Gaussiana e Lorenziana).
        Richiede scipy.special.wofz.
        amp   : Fattore di scala ampiezza
        x0    : Centro
        sigma : Larghezza Gaussiana
        gamma : Larghezza Lorenziana
        """
        z = ((x - x0) + 1j*gamma) / (sigma * np.sqrt(2))
        return amp * np.real(wofz(z)) / (sigma * np.sqrt(2*np.pi))

    @staticmethod
    def lognormal(x, amp, s, scale):
        """
        Distribuzione Log-Normale (asimmetrica con coda a destra).
        amp   : Fattore di scala
        s     : Parametro di forma (sigma del logaritmo)
        scale : Parametro di scala (exp(mu) del logaritmo)
        """
        # Protezione per x <= 0 dove log non è definito
        x = np.where(x > 0, x, 1e-9) 
        return (amp / (s * x * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((np.log(x) - np.log(scale)) / s)**2)

    @staticmethod
    def exponential_pdf(x, amp, lambd):
        """
        Distribuzione Esponenziale (decadimento).
        amp    : Ampiezza iniziale
        lambd  : Rate parameter (1/tau)
        """
        return amp * lambd * np.exp(-lambd * x)

    @staticmethod
    def skewed_gaussian(x, amp, mu, sigma, alpha):
        """
        Gaussiana "storta" (Skewed Gaussian).
        amp   : Ampiezza
        mu    : Posizione
        sigma : Larghezza
        alpha : Fattore di asimmetria (skewness). 0 = normale, >0 coda a dx, <0 coda a sx.
        """
        # Parte gaussiana standard
        pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
        # Parte CDF per lo skew
        cdf = 0.5 * (1 + erf(alpha * (x - mu) / (sigma * np.sqrt(2))))
        return amp * 2 * pdf * cdf


def calcola_cost(espressione):
    """
    Valuta un'espressione matematica stringa in sicurezza usando numpy.
    
    Args:
        espressione: stringa della formula, es. "1/np.sqrt(np.pi)"
        
    Returns:
        Il risultato numerico calcolato o None in caso di errore.
    """
    try:
        # Pulizia della stringa
        formula = espressione.strip()

        # Ambiente sicuro: carichiamo numpy e rimuoviamo builtins pericolosi
        ambiente_sicuro = {
            "np": np,
            "__builtins__": None
        }

        # Valuta la formula
        # Nota: eval restituisce il tipo di dato risultante (float, int, o np.array)
        return float(eval(formula, {"__builtins__": None}, ambiente_sicuro))

    except SyntaxError as e:
        print(f"Errore di sintassi nell'espressione '{espressione}': {e}")
    except NameError as e:
        print(f"Errore di nome (variabile non definita) in '{espressione}': {e}")
    except Exception as e:
        print(f"Errore durante il calcolo di '{espressione}': {e}")
    
    return None


def calcola(data, data2, fun_data, parameters, datax=None):
    """
    Valuta una formula numerica in sicurezza usando numpy.
    Supporta x (data), x2 (data2), xaxis (datax) e parametri custom.
    
    Args:
        data: array-like, valori di x
        data2: array-like o None, valori di x2 (deve avere la stessa lunghezza di data)
        fun_data: stringa della formula, es. "x + x2 * k"
        parameters: stringa dei parametri, es. "k=0.1,OFFSET=5"
        datax: array-like o None, valori per l'asse x (xaxis)
        
    Returns:
        np.array dei risultati o None in caso di errore
    """
    try:
        formula = fun_data.strip()

        # 1. Parsing dei parametri generici: "TEMP=100,k=0.1" -> {"TEMP":100.0, "k":0.1}
        param_dict = {}
        if parameters:
            for item in parameters.split(","):
                if "=" in item:
                    key, val = item.split("=", 1)
                    key = key.strip()
                    try:
                        val = float(calcola_cost(val.strip()))
                        param_dict[key] = val
                    except ValueError:
                        print(f"Attenzione: Impossibile convertire il parametro '{key}' in float.")

        # 2. Creazione ambiente base
        # Converto sempre 'data' in array numpy float per coerenza
        ambiente_sicuro = {
            "x": np.array(data, dtype=float),
            "np": np,
            "__builtins__": None
        }

        # 3. Aggiunta opzionale di xaxis
        if datax is not None:
            ambiente_sicuro["xaxis"] = np.array(datax, dtype=float)

        # 4. Aggiunta opzionale di x2 (data2)
        # Se la formula contiene 'x2' ma data2 è None, eval solleverà un NameError (gestito sotto)
        if data2 is not None:
            ambiente_sicuro["x2"] = np.array(data2, dtype=float)

        # 5. Aggiungo i parametri parsati all'ambiente
        ambiente_sicuro.update(param_dict)

        # 6. Valuta la formula
        return eval(formula, {"__builtins__": None}, ambiente_sicuro)

    except SyntaxError as e:
        print(f"Errore di sintassi nella formula '{fun_data}': {e}")
    except NameError as e:
        # Questo cattura il caso in cui usi 'x2' nella formula ma passi data2=None
        print(f"Errore: variabile non trovata nella formula '{fun_data}'. Hai passato tutti i dati necessari? Dettagli: {e}")
    except ValueError as e:
        # Cattura errori di dimensioni diverse tra gli array (es. len(x) != len(x2))
        print(f"Errore di valore (probabile mismatch dimensioni array): {e}")
    except Exception as e:
        print(f"Errore generico durante l'elaborazione della formula '{fun_data}': {e}")
    
    return None


class Helper:
    @staticmethod
    def add_label(parent, text, row, col, label_font=None, colspan=1, padx=5, pady=5, sticky="w", tooltip=None, colorbg=None, colorfg= None):
        lbl = tk.Label(parent, text=text, font=label_font or dim.label_font(LABEL_SIZE))
        if colorbg is not None:
            lbl.configure(bg=colorbg)
        if colorfg is not None:
            lbl.configure(bg=colorfg)
        lbl.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(lbl, tooltip)
        return lbl, col + colspan
    
    
    @staticmethod
    def add_label_entry(parent, label_text, variable, row, col, entry_width=None,
                  label_font=None, entry_font=None, padx=5, pady=5, sticky="w", rowspan=1, columnspan=1, tooltip=None, colorbg=None, colorfg= None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky, colorbg=colorbg, colorfg=colorfg)
        entry = tk.Entry(parent, textvariable=variable, font=entry_font or dim.entry_font(ENTRY_SIZE), width=entry_width)
        entry.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(entry, tooltip)
        return entry, col+1

    @staticmethod
    def add_entry(parent, variable, row, col, entry_width=None, entry_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        entry = tk.Entry(parent, textvariable=variable, font=entry_font or dim.entry_font(ENTRY_SIZE), width=entry_width)
        entry.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(entry, tooltip)
        return entry, col+1
    
    
    @staticmethod
    def add_text(parent, variable, row, col, width=0, height=5, entry_font=None,
                padx=5, pady=5, sticky="w", tooltip=None):
        text_widget = tk.Text(parent, width=width, height=height, font=entry_font or dim.entry_font(ENTRY_SIZE))
        text_widget.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)

        def on_text_change(event=None):
            variable.set(text_widget.get("1.0", "end-1c"))  # aggiorna la variabile
            text_widget.edit_modified(False)  # resetta il flag di modifica

        text_widget.bind("<<Modified>>", on_text_change)

        if tooltip:
            ToolTip(text_widget, tooltip)
        return text_widget, col+1


    @staticmethod
    def add_label_text(parent, label_text, variable, row, col, width=50, height=5, entry_font=None, label_font=None,
                padx=5, pady=5, sticky="w", tooltip=None, colorbg=None, colorfg= None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky, colorbg=colorbg, colorfg=colorfg)
        text_widget = tk.Text(parent, width=width, height=height, font=entry_font or dim.entry_font(ENTRY_SIZE))
        text_widget.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)

        def on_text_change(event=None):
            variable.set(text_widget.get("1.0", "end-1c"))  # aggiorna la variabile
            text_widget.edit_modified(False)  # resetta il flag di modifica

        text_widget.bind("<<Modified>>", on_text_change)

        if tooltip:
            ToolTip(text_widget, tooltip)
        return text_widget, col+1

    @staticmethod
    def add_label_optionmenu(parent, label_text, variable, options, row, col, colspan=1,
                       label_font=None, padx=5, pady=5, sticky="w", tooltip=None, colorbg=None, colorfg= None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky, colorbg=colorbg, colorfg=colorfg)
        opt = tk.OptionMenu(parent, variable, *options)
        opt.config(font=label_font or dim.label_font(LABEL_SIZE), bg=colorbg)
        opt["menu"].config(bg=colorbg)
        opt.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(opt, tooltip)
        return opt, col+1

    
    @staticmethod
    def add_optionmenu(parent, variable, options, row, col, colspan=1,
                       label_font=None, padx=5, pady=5, sticky="w", tooltip=None, colorbg=None):
        opt = tk.OptionMenu(parent, variable, *options)
        opt.config(font=label_font or dim.label_font(LABEL_SIZE), bg=colorbg)
        opt["menu"].config(bg=colorbg)
        opt.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(opt, tooltip)
        return opt, col+1
    
    @staticmethod
    def add_button(parent, text, command, row=None, col=None, colspan=1, use_pack=False,
                   label_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        btn = tk.Button(parent, text=text, font=label_font, command=command)
        if use_pack:
            btn.pack(padx=dim.s(padx), pady=dim.s(pady))
        else:
            btn.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(btn, tooltip)
        return btn, col+1

    @staticmethod
    def add_checkbutton(parent, label_text, variable, row, col, colspan=1,
                        label_font=None, padx=5, pady=5, sticky="w", tooltip=None, colorbg=None):
        chk = tk.Checkbutton(parent, text=label_text, variable=variable, font=label_font, bg=colorbg)
        chk.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(chk, tooltip)
        return chk, col+1

    @staticmethod
    def add_spinbox(parent, variable, from_, to, increment=1, row=0, col=0, format_str=None,
                    entry_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        spin_args = {"from_": from_, "to": to, "increment": increment, "textvariable": variable}
        if format_str:
            spin_args["format"] = format_str
        spin = tk.Spinbox(parent, **spin_args, font=entry_font or dim.entry_font(ENTRY_SIZE))
        spin.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(spin, tooltip)
        return spin, col+1

    @staticmethod
    def add_scale(parent, variable, from_, to, orient="horizontal", resolution=1, row=0, col=0, colspan=1,
                  label_font=("Arial", "7"), padx=5, pady=5, sticky="ew", tooltip=None, lenght=100, width=15,sliderlength=30, colorbg=None):
        scale = tk.Scale(parent, from_=from_, to=to, orient=orient, resolution=resolution,
                         variable=variable, font=label_font, length=dim.s(lenght), width=dim.s(width), sliderlength=dim.s(sliderlength), bg=colorbg)
        scale.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(scale, tooltip)
        return scale, col+1

    @staticmethod
    def add_color(parent, color_var, row, col, padx=5, pady=5, sticky="w", tooltip=None):
        color_index = col_index[color_var.get()] if color_var.get() in col_index else 0
        color_frame = create_color_menu(parent, color_var, color_index)
        color_frame.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(color_frame, tooltip)
        return color_frame, col+1

    @staticmethod
    def add_copy_text(parent, testo_da_copiare, row, col, padx=5, pady=5, sticky="w", tooltip=None):
        entry = tk.Entry(parent,readonlybackground=parent.cget("bg"),relief="flat",borderwidth=0)
        entry.insert(0, testo_da_copiare)
        entry.config(state="readonly")
        entry.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(entry, tooltip)
        return entry, col+1

    
class ToggleSwitch(tk.Canvas):
    def __init__(self, master, variable, options, tooltip_text=None, width=60, height=30, bg_off="#ccc", bg_on="#4cd137", circle_color="white"):
        super().__init__(master, width=width, height=height, bg=master["bg"], highlightthickness=0)
        self.variable = variable
        self.options = options
        self.width = width
        self.height = height
        self.bg_off = bg_off
        self.bg_on = bg_on
        self.circle_color = circle_color
        self.state = self.variable.get() == self.options[1]

        # Background rettangolare arrotondato
        self.rect = self.create_rounded_rect(2, 2, width-2, height-2, radius=height//2, fill=self.bg_on if self.state else self.bg_off)

        # Cerchio mobile
        circle_radius = height - 4
        self.circle = self.create_oval(
            2 if not self.state else width - circle_radius - 2,
            2,
            2 + circle_radius,
            2 + circle_radius,
            fill=self.circle_color, outline=""
        )

        # Click per toggle
        self.bind("<Button-1>", self.toggle)

        # Tooltip opzionale
        if tooltip_text:
            ToolTip(self, tooltip_text)

    def create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def toggle(self, event=None):
        self.state = not self.state
        self.variable.set(self.options[1] if self.state else self.options[0])
        self.update_visual()

    def update_visual(self):
        # Aggiorna colore di sfondo
        self.itemconfig(self.rect, fill=self.bg_on if self.state else self.bg_off)
        # Aggiorna posizione cerchio
        circle_radius = self.height - 4
        x1 = 2 if not self.state else self.width - circle_radius - 2
        x2 = x1 + circle_radius
        self.coords(self.circle, x1, 2, x2, 2 + circle_radius)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # rimuove bordi e titolo
        tw.wm_geometry(f"+{x}+{y}")
        tw.wm_attributes("-alpha", 0.85)  # quasi trasparente
        label = tk.Label(tw, text=self.text, background="#000000", foreground="white",
                 relief="solid", borderwidth=1, padx=5, pady=2)
        label.pack()

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


class DATALOAD:
    def _get_filter_mask(self, df, colonna, criterio_str):
        # Definiamo gli operatori
        operatori = {
            '>=': lambda x, v: x >= v, 
            '<=': lambda x, v: x <= v, 
            '!=': lambda x, v: x != v, 
            '==': lambda x, v: x == v, # Aggiunto == per sicurezza
            '=':  lambda x, v: x == v, 
            '>':  lambda x, v: x > v, 
            '<':  lambda x, v: x < v
        }
        
        maschera_totale = pd.Series(True, index=df.index)
        sotto_condizioni = str(criterio_str).split(',')
        col_data = df[colonna]
        is_numeric = pd.api.types.is_numeric_dtype(col_data)

        for cond in sotto_condizioni:
            cond = cond.strip()
            if not cond: continue
            
            target_op = None
            val_str = cond
            
            # ORDINAMENTO CHIAVI: Fondamentale iterare prima sulle chiavi più lunghe 
            # (es. controllare '>=' prima di '>') altrimenti '>' matcha l'inizio di '>='
            for op in sorted(operatori.keys(), key=len, reverse=True):
                if cond.startswith(op):
                    target_op = operatori[op]
                    val_str = cond[len(op):].strip()
                    break
            
            # Se non trova operatore, assume uguaglianza
            if target_op is None: 
                target_op = lambda x, v: x == v
            
            try:
                valore = float(val_str) if is_numeric else val_str
                maschera_totale = maschera_totale & target_op(col_data, valore)
            except ValueError:
                raise ValueError(f"Valore non valido: {val_str}")
                
        return maschera_totale


    def read(self, file_path, x, y, xerr, yerr, x2, y2, x_min, x_max, y_min, y_max, 
             filters1="None", filters2="None", filters3="None", filters4="None", 
             x_fun="", x_par="", y_fun="", y_par=""): # Aggiunti default arguments vuoti per sicurezza e ':'
        
        # --- 1. CARICAMENTO FILE ---
        try:
            if file_path.endswith('.txt'): file_path = convert_file_to_csv(file_path)
            if file_path.endswith('.csv'): df = pd.read_csv(file_path)
            elif file_path.endswith('.xml'): df = pd.read_xml(file_path)
            else: raise ValueError("Formato non supportato")
        except Exception as e:
            messagebox.showerror("Errore caricamento", str(e))
            return None, None, None, None 
        
        df = df.replace(r'^\s*-?nan\s*$', np.nan, regex=True)

        # Pulizia variabili input
        inputs = {'x': x, 'y': y, 'xerr': xerr, 'yerr': yerr, 'x2': x2, 'y2': y2}
        for k, v in inputs.items():
            if str(v) == "None": inputs[k] = None
        
        x, y, xerr, yerr, x2, y2 = inputs['x'], inputs['y'], inputs['xerr'], inputs['yerr'], inputs['x2'], inputs['y2']

        # --- CHECK COLONNE ESISTENTI ---
        for col_name in [x, y, xerr, yerr, x2, y2]:
            if col_name and col_name not in df.columns:
                messagebox.showerror("Errore Colonna", f"La colonna '{col_name}' non esiste nel file.")
                return None, None, None, None

        # --- 2. APPLICAZIONE FILTRI AVANZATI ---
        lista_filtri = [filters1, filters2, filters3, filters4]

        for i, current_filter in enumerate(lista_filtri):
            if current_filter == "None" or current_filter is None: continue
            
            col_cat = current_filter.get('cat')
            val_expr = current_filter.get('val')
            col_compare = current_filter.get('compare')

            if not col_cat or str(col_cat) == "None": continue
            if not val_expr:
                messagebox.showerror("Errore", f"Filtro #{i+1}: Valore mancante.")
                return None, None, None, None
            if col_cat not in df.columns:
                messagebox.showerror("Errore", f"Colonna '{col_cat}' non trovata.")
                return None, None, None, None

            try:
                maschera = None
                
                # CASO A: COMPARE ATTIVO (confronto tra due colonne)
                if col_compare and str(col_compare) != "None":
                    if col_compare not in df.columns:
                        messagebox.showerror("Errore", f"Colonna confronto '{col_compare}' non trovata.")
                        return None, None, None, None
                    
                    local_env = {'x': df[col_cat], 'y': df[col_compare], 'np': np, 'pd': pd}
                    expr = str(val_expr).strip()
                    
                    simple_ops = ['<', '>', '<=', '>=', '==', '!=', '=']
                    if expr in simple_ops:
                        op = '==' if expr == '=' else expr
                        final_expr = f"x {op} y"
                    else:
                        final_expr = expr

                    try:
                        maschera = eval(final_expr, {"__builtins__": None}, local_env)
                    except Exception as eval_err:
                        raise ValueError(f"Espressione non valida: '{final_expr}'.\n{eval_err}")

                # CASO B: COMPARE SPENTO (valore diretto)
                else:
                    maschera = self._get_filter_mask(df, col_cat, val_expr)

                if not isinstance(maschera, (pd.Series, np.ndarray)):
                     raise ValueError("Il filtro non ha restituito vero/falso.")

                df = df[maschera] 

                if df.empty:
                    messagebox.showwarning("Nessun Dato", f"Il Filtro #{i+1} ha escluso tutti i dati.")
                    return None, None, None, None

            except Exception as e:
                messagebox.showerror("Errore Filtro", f"Errore nel Filtro #{i+1}:\n{str(e)}")
                return None, None, None, None

        # --- 3. PREPARAZIONE DATI --- 
        cols_to_check = [c for c in [x, y] if c is not None]
        if cols_to_check: 
            df = df.dropna(subset=cols_to_check)
        
        if x is not None and pd.api.types.is_numeric_dtype(df[x]):
            df = df.sort_values(by=x)
            
        try:
            if x and x_min and str(x_min).strip(): df = df[df[x] >= float(x_min)]
            if x and x_max and str(x_max).strip(): df = df[df[x] <= float(x_max)]
            if y and y_min and str(y_min).strip(): df = df[df[y] >= float(y_min)]
            if y and y_max and str(y_max).strip(): df = df[df[y] <= float(y_max)]
        except ValueError:
            messagebox.showerror("Errore", "Range non numerici")
            return None, None, None, None
        
        if df.empty:
             messagebox.showwarning("Nessun Dato", "Filtri Range hanno svuotato il dataset.")
             return None, None, None, None

        # --- CORREZIONE CRITICA: RIMOSSE LE VIRGOLE FINALI ---
        # Prima era: datax = df[x].values if x else None, (che crea una tupla)
        datax = df[x].values if x else None
        datay = df[y].values if y else None
        xerr = df[xerr].values if xerr else None
        yerr = df[yerr].values if yerr else None
        
        # Estraggo x2 e y2 per i calcoli, ma non li ritorno alla fine (come da codice originale)
        datax2 = df[x2].values if x2 else None
        datay2 = df[y2].values if y2 else None

        # --- CALCOLI ESTERNI ---
        # Nota: La funzione 'calcola' deve essere definita nel tuo script principale
        if x_fun and str(x_fun).strip():
            # Passiamo datax pulito (numpy array), non una tupla
            datax = calcola(datax, datax2, x_fun, x_par)
            
        if y_fun and str(y_fun).strip():
            # Se calcola richiede datax aggiornato come contesto
            datay = calcola(datay, datay2, y_fun, y_par, datax) 

        return datax, datay, xerr, yerr
        
    

def create_color_menu(parent, color_var, color_index, allow_none=True):
    class CustomCombobox(tk.Frame):
        def __init__(self, master, values, variable, **kwargs):
            super().__init__(master, **kwargs)
            self.values = values
            if allow_none:
                self.values = [None] + self.values  # aggiunge None come prima opzione
            self.variable = variable
            self.variable.set(self.values[color_index] if color_index < len(self.values) else self.values[0])
            self.dropdown_open = False

            # Canvas to show selected color
            self.canvas = tk.Canvas(self, width=dim.s(36), height=dim.s(36), bg="white", highlightthickness=0)
            self.canvas.pack(side="left", padx=(dim.s(0), dim.s(5)))
            self.update_display()

            # Button to open dropdown
            self.button = tk.Button(self, 
                        text="▼", 
                        width=2,       # Larghezza in caratteri (prova 1 o 2)
                        bd=1,          # Bordo sottile
                        padx=0,        # Rimuove spazio orizzontale interno
                        pady=0,        # Rimuove spazio verticale interno
                        highlightthickness=0, # Rimuove il bordo del focus
                        command=self.toggle_dropdown)
            self.button.pack(side="left")

        def update_display(self):
            selected_color = self.variable.get()
            self.canvas.delete("color_circle")
            fill_color = selected_color if selected_color is not None else "white"
            if selected_color is None or selected_color == "None":
                fill_color = ""  # canvas trasparente
            else:
                fill_color = selected_color

            self.canvas.create_oval(dim.s(2), dim.s(2), dim.s(34), dim.s(34), fill=fill_color, outline="", tags="color_circle")


        def toggle_dropdown(self):
            if self.dropdown_open:
                self.dropdown_window.destroy()
                self.dropdown_open = False
            else:
                self.open_dropdown()

        def open_dropdown(self):
            self.dropdown_window = tk.Toplevel(self)
            self.dropdown_window.overrideredirect(True)
            self.dropdown_window.geometry(f"100x380+{self.winfo_rootx()}+{self.winfo_rooty() + self.winfo_height()}")

            # Listbox to display color options
            listbox = tk.Listbox(self.dropdown_window, height=min(len(self.values), 10), selectmode="single")
            listbox.pack(side="left", fill="both", expand=True)

            # Scrollbar for listbox
            scrollbar = tk.Scrollbar(self.dropdown_window, command=listbox.yview)
            scrollbar.pack(side="right", fill="y")
            listbox.config(yscrollcommand=scrollbar.set)

            # Populate listbox with colors
            for color in self.values:
                display_text = "None" if color is None else color
                listbox.insert("end", display_text)

            def select_color(event):
                selected_index = listbox.curselection()
                if selected_index:
                    self.variable.set(self.values[selected_index[0]])
                    self.update_display()
                    self.dropdown_window.destroy()
                    self.dropdown_open = False

            listbox.bind("<<ListboxSelect>>", select_color)

            self.dropdown_open = True

    # Create a frame with a custom combobox
    frame = tk.Frame(parent)
    combobox = CustomCombobox(frame, values=COLOR, variable=color_var)
    combobox.pack()
    return frame

class Dimension:
    def __init__(self, root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        scale_x = screen_width / BASE_WIDTH
        scale_y = screen_height / BASE_HEIGHT
        self.scale = min(scale_x, scale_y)

        # Imposta la finestra iniziale
        root.geometry(f"{self.s(720)}x{self.s(800)}")

    def s(self, x):
        """Scala un valore in base alla risoluzione dello schermo"""
        return int(x * self.scale)

    def label_font(self, size=16):
        """Restituisce una tupla font scalata per Label"""
        return ("Arial", self.s(size))

    def entry_font(self, size=14):
        """Restituisce una tupla font scalata per Entry"""
        return ("Arial", self.s(size))
    

root = tk.Tk()
dim = Dimension(root)