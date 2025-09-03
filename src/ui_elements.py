import tkinter as tk
from tkinter import Canvas, Toplevel, Listbox, Scrollbar
import re
import csv
import tempfile
import numpy as np

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
REGRESSION_FUNCTIONS = ["Linear", "Quadratic", "Polynomial", "Logarithmic", "Exponential", "Power law", "Sigmoid"]

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
    def linear(x, a, b):
        return a*x + b

    def quadratic(x, a, b, c):
        return a*x**2 + b*x + c

    def polynomial(x, *coeffs):
        # coeffs = [a_n, ..., a1, a0]
        return np.poly1d(coeffs)(x)

    def logarithmic(x, a, b):
        return a * np.log(x) + b

    def exponential(x, a, b):
        return a * np.exp(b*x)

    def powerlaw(x, a, b):
        return a * np.power(x, b)

    def sigmoid(x, L, x0, k):
        return L / (1 + np.exp(-k*(x-x0)))

import numpy as np

def calcola(data, fun_data, parameters):
    """
    Valuta una formula numerica in sicurezza usando numpy, con parametri generici.
    
    Args:
        data: array-like, valori di x
        fun_data: stringa della formula, es. "TEMP*np.exp(-k*x) + OFFSET"
        parameters: stringa dei parametri, es. "TEMP=100,k=0.1,OFFSET=5"
        
    Returns:
        np.array dei risultati della formula valutata
    """
    try:
        formula = fun_data.strip()

        # Parsing dei parametri generici: "TEMP=100,k=0.1" -> {"TEMP":100.0, "k":0.1}
        param_dict = {}
        if parameters:
            for item in parameters.split(","):
                if "=" in item:
                    key, val = item.split("=", 1)  # split solo sul primo '='
                    key = key.strip()
                    val = float(val.strip())
                    param_dict[key] = val

        # Ambiente sicuro per eval
        ambiente_sicuro = {
            "x": np.array(data, dtype=float),
            "np": np,
            "__builtins__": None
        }

        # Aggiungo i parametri all'ambiente
        ambiente_sicuro.update(param_dict)

        # Valuta la formula
        return eval(formula, {"__builtins__": None}, ambiente_sicuro)

    except SyntaxError as e:
        print(f"Errore di sintassi nella formula '{fun_data}': {e}")
    except NameError as e:
        print(f"Errore di nome nella formula '{fun_data}': {e}")
    except Exception as e:
        print(f"Errore generico durante l'elaborazione della formula '{fun_data}': {e}")
    return None


class Helper:
    @staticmethod
    def add_label(parent, text, row, col, label_font=None, colspan=1, padx=5, pady=5, sticky="w", tooltip=None):
        lbl = tk.Label(parent, text=text, font=label_font or dim.label_font(LABEL_SIZE))
        lbl.grid(row=row, column=col, columnspan=colspan, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(lbl, tooltip)
        return lbl, col+1

    @staticmethod
    def add_label_entry(parent, label_text, variable, row, col, entry_width=None,
                  label_font=None, entry_font=None, padx=5, pady=5, sticky="w", rowspan=1, columnspan=1, tooltip=None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky)
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
                padx=5, pady=5, sticky="w", tooltip=None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky)
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
    def add_label_optionmenu(parent, label_text, variable, options, row, col,
                       label_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        _, col = Helper.add_label(parent, label_text, row, col, label_font=label_font, padx=padx, pady=pady, sticky=sticky)
        opt = tk.OptionMenu(parent, variable, *options)
        opt.config(font=label_font or dim.label_font(LABEL_SIZE))
        opt.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
        if tooltip:
            ToolTip(opt, tooltip)
        return opt, col+1

    @staticmethod
    def add_optionmenu(parent, variable, options, row, col,
                       label_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        opt = tk.OptionMenu(parent, variable, *options)
        opt.config(font=label_font or dim.label_font(LABEL_SIZE))
        opt.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
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
                        label_font=None, padx=5, pady=5, sticky="w", tooltip=None):
        chk = tk.Checkbutton(parent, text=label_text, variable=variable, font=label_font)
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
    def add_scale(parent, variable, from_, to, orient="horizontal", resolution=1, row=0, col=0,
                  label_font=("Arial", "7"), padx=5, pady=5, sticky="ew", tooltip=None, lenght=None):
        scale = tk.Scale(parent, from_=from_, to=to, orient=orient, resolution=resolution,
                         variable=variable, font=label_font, length=lenght)
        scale.grid(row=row, column=col, padx=dim.s(padx), pady=dim.s(pady), sticky=sticky)
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
            self.canvas = tk.Canvas(self, width=20, height=20, bg="white", highlightthickness=0)
            self.canvas.pack(side="left", padx=(0, 5))
            self.update_display()

            # Button to open dropdown
            self.button = tk.Button(self, text="▼", width=1, command=self.toggle_dropdown)
            self.button.pack(side="left")

        def update_display(self):
            selected_color = self.variable.get()
            self.canvas.delete("color_circle")
            fill_color = selected_color if selected_color is not None else "white"
            if selected_color is None or selected_color == "None":
                fill_color = ""  # canvas trasparente
            else:
                fill_color = selected_color

            self.canvas.create_oval(2, 2, 18, 18, fill=fill_color, outline="", tags="color_circle")


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