import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use("TkAgg")
from ui_elements import dim, MARKER, LINE, LOG, YN, TF, LEGEND, COLOR, ORIENTATION, ALIGN, PLOT, REGRESSION_FUNCTIONS, FUNCTION, HISTTYPE, AXIS, Helper, Functions, DATALOAD
from ui_elements import convert_file_to_csv, ToggleSwitch
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from ui_elements import calcola
import os
BASE_DIR = os.path.dirname(__file__)

ui = Helper
loader = DATALOAD()


class DataOptions:
    def __init__(self, root, inset_counter, data_id, file_path, column, data_options, all_data_id, upload=False):
        self.root = root
        self.upload = upload
        
        # Options dictionary
        self.data_options = {
            "data_id": data_id,
            "inset": inset_counter,
            "file path": file_path,            
            "plot_select": tk.StringVar(value="plot"),
            "show/hide": tk.StringVar(value="1"),
            "common": {
                "x": tk.StringVar(value=column[0]),
                "x2": tk.StringVar(value="None"),
                "x_min": tk.StringVar(value=""),
                "x_max": tk.StringVar(value=""),
                "x_err": tk.StringVar(value="None"),
                "label": tk.StringVar(),
                "y_function": tk.StringVar(value=""),
                "y_parameters": tk.StringVar(value=""),
                "x_function": tk.StringVar(value=""),
                "x_parameters": tk.StringVar(value=""),
                "color": tk.StringVar(value=COLOR[0]),
                "alpha": tk.StringVar(value="1"),
                "col_filter1": tk.StringVar(value="None"),
                "filter1": tk.StringVar(value=""), 
                "col_compare_filter1": tk.StringVar(value="None"),
                "col_filter2": tk.StringVar(value="None"),
                "filter2": tk.StringVar(value=""), 
                "col_compare_filter2": tk.StringVar(value="None"),
                "col_filter3": tk.StringVar(value="None"),
                "filter3": tk.StringVar(value=""), 
                "col_compare_filter3": tk.StringVar(value="None"),
                "col_filter4": tk.StringVar(value="None"),
                "filter4": tk.StringVar(value=""), 
                "col_compare_filter4": tk.StringVar(value="None"), 
            },
            "fit" : {
                "plot_reg": tk.StringVar(value="No"),
                "type": tk.StringVar(value=REGRESSION_FUNCTIONS[0]),
                "line": tk.StringVar(value=LINE[0]),
                "lw": tk.StringVar(value="1"),
                "color": tk.StringVar(value=COLOR[0]),
                "alpha": tk.StringVar(value="1"),
                "label": tk.StringVar(value=""),
                "params": {}                    
            },
            "plot": {
                "y": tk.StringVar(value=column[0]),
                "y2": tk.StringVar(value="None"),
                "y_min": tk.StringVar(value=""),
                "y_max": tk.StringVar(value=""),
                "y_err": tk.StringVar(value="None"),
                "marker": tk.StringVar(value=MARKER[0]),
                "ms": tk.StringVar(value="5"),
                "mfc": tk.StringVar(value="No"),
                "mfcolor": tk.StringVar(value=COLOR[0]),
                "line": tk.StringVar(value="None"),
                "lw": tk.StringVar(value="1"),
                "errorbar": {
                    "ecolor": tk.StringVar(value=COLOR[0]),
                    "elinewidth": tk.StringVar(value=1.5),
                    "capsize": tk.StringVar(value=3),
                    "capthick": tk.StringVar(value=1.5)
                }
            },
            "hist": {
                "histtype": tk.StringVar(value=HISTTYPE[0]),
                "bins": tk.StringVar(value="10"),
                "align": tk.StringVar(value=ALIGN[0]),
                "density": tk.StringVar(value="True"),
                'orientation': tk.StringVar(value=ORIENTATION[0]), 
                'cumulative': tk.StringVar(value="False"), 
                'bottom': tk.StringVar(value=0), 
                'rwidth': tk.StringVar(value=1),
                'contour_color': tk.StringVar(value='None'),
                'contour_alpha': tk.StringVar(value="1"),
                'contour_width': tk.StringVar(value="1"),
                'contour_line': tk.StringVar(value=LINE[0]),
                'tick_par' : {
                    'axis': tk.StringVar(value='both'),          # Applica a 'x', 'y' o 'both'
                    'direction': tk.StringVar(value='out'),      # Trattino dentro, fuori o a cavallo della linea
                    'length': tk.StringVar(value=4),            # Lunghezza del trattino
                    'width': tk.StringVar(value=0.5),              # Spessore del trattino
                    'color': tk.StringVar(value='black'),         # Colore del trattino
                    'labelcolor': tk.StringVar(value='black'),     # Colore del testo
                    'labelsize': tk.StringVar(value=10),         # Dimensione del testo
                    'pad': tk.StringVar(value=5)                # Distanza tra testo e asse                  
                }
            },
            "scatter": {
                "orientation": tk.StringVar(value=ORIENTATION[0]),
                "size": tk.StringVar(value="5"),
                "cmap": tk.StringVar(value="viridis")
            },
            "bar": {
                "orientation": tk.StringVar(value=ORIENTATION[0]),
                "width": tk.StringVar(value="0.8"),
                "align": tk.StringVar(value=ALIGN[0])
            },
            "pie": {
                "explode": tk.StringVar(value="0,0,0,0"),
                "autopct": tk.StringVar(value="%1.1f%%"),
                "startangle": tk.StringVar(value="90")
            },
            "boxplot": {
                "vert": tk.StringVar(value="True"),
                "patch_artist": tk.StringVar(value="True")
            },
            "violin": {
                "showmeans": tk.StringVar(value="True"),
                "showextrema": tk.StringVar(value="True")
            },
            "heatmap": {
                "cmap": tk.StringVar(value="viridis"),
                "interpolation": tk.StringVar(value="nearest")
            },
            "contour": {
                "levels": tk.StringVar(value="10"),
                "cmap": tk.StringVar(value="viridis")
            },
            "quiver": {
                "scale": tk.StringVar(value="1"),
                "scale_units": tk.StringVar(value="xy"),
                "angles": tk.StringVar(value="xy")
            },
            "polar": {
                "theta": tk.StringVar(value=column[0]),
                "r": tk.StringVar(value=column[1]),
                "theta_units": tk.StringVar(value="radians"),
                "r_units": tk.StringVar(value="linear")
            },
            "stack": {
                "x": tk.StringVar(value=column[0]),
                "y": tk.StringVar(value=column[1]),
                "stacked": tk.StringVar(value="True")
            }
        }
        #"plot", "hist", "scatter", "bar", "pie", "boxplot", "violin", "heatmap", "contour", "quiver", "polar", "stack"
        self.options(data_options,data_id,column,all_data_id)
        data_options[data_id] = self.data_options
        
    def options(self, data_options, data_id, column, all_data_id):
        # Main dataset frame: expands horizontally
        frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1, bg="lightblue")
        frame.pack(padx=dim.s(5), pady=dim.s(5), fill="x", expand=True)


        # --- Frame for specific options: takes full width
        specific_frame = tk.Frame(frame, bg="lightblue")
        specific_frame.grid(row=1, column=0, columnspan=5, sticky="ew")
        specific_frame.grid_columnconfigure(0, weight=1)  # to stretch internally, if necessary
        
        if self.upload:
            self.data_options = data_options[data_id]

        # --- Row 1: File info ---
        trash_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "cestino.png")).subsample(20, 20)
        tk.Button(
            frame, image=trash_icon,
            command=lambda: self.remove_data(frame, data_id, all_data_id, data_options)
        ).grid(row=0, column=0, padx=dim.s(5), pady=dim.s(5), sticky="w")
        if not hasattr(self, 'trash_icons'):
            self.trash_icons = []
        self.trash_icons.append(trash_icon)

        file_label = tk.Label(frame,text=f"File: {self.data_options['file path'].split('/')[-1]}",anchor="w", font=("Arial", 12, "bold"), bg="lightblue")
        file_label.grid(row=0, column=1, padx=dim.s(5), pady=dim.s(5), sticky="ew")

        self.tool_frame = tk.Frame(frame, bg="lightblue")
        self.tool_frame.grid(row=0,column=2,sticky="ew")
        ui.add_checkbutton(self.tool_frame, "Show plot", self.data_options["show/hide"], row=0, col=0, label_font=dim.label_font(14), tooltip="Mostra/Nascondi plot", colorbg="lightblue")
        ui.add_label_optionmenu(self.tool_frame, "Mode:", self.data_options["plot_select"], PLOT, row=0, col=2, colorbg="lightblue")
        
        # Toggle button
        toggle_button = tk.Button(self.tool_frame, text="Esegui Fit", command=lambda: self.toggle_regression(specific_frame, toggle_button))
        toggle_button.grid(row=0, column=4, sticky="w", padx=dim.s(5), pady=dim.s(5))
        # Button to create and show regression frame


        self.expanded = True  
        # Arrow button (initially "▼")
        self.toggle_button = tk.Button(
            self.tool_frame, text="▼", width=2, command=lambda: self.toggle_frame(specific_frame)
        )
        self.toggle_button.grid(row=0, column=5, padx=dim.s(5), pady=dim.s(5), sticky="e")
        
        

        # ⬅️ GIVE WEIGHT TO COLUMN 1 (the one with the label)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)  # expands to fill
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=0)

    
        # Function to update specific options
        def refresh_options(*args):
            # Clear previous specific widgets
            for widget in specific_frame.grid_slaves():
                widget.destroy()

            mode = self.data_options["plot_select"].get()
            row, col = 1, 0

            if mode == "plot":
                # Horizontally scrollable canvas
                self.plot_config(specific_frame,column)
            elif mode == "hist":
                self.hist_config(specific_frame,column)
            elif mode == "scatter":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["common"]["y"], column, row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Size:", self.data_options["scatter"]["size"], row=row, col=col)
                _, col = ui.add_color(specific_frame, "Color:", self.data_options["common"]["color"], row=row, col=col, tooltip="Color")
                _, col = ui.add_label_entry(specific_frame, self.data_options["common"]["alpha"], row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Orientation:", self.data_options["scatter"]["orientation"], ORIENTATION, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Colormap:", self.data_options["scatter"]["cmap"], ["viridis", "plasma", "inferno", "magma", "cividis"], row=row, col=col)
                
            elif mode == "bar":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["bar"]["y"], column, row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Width:", self.data_options["bar"]["width"], row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Orientation:", self.data_options["bar"]["orientation"], ORIENTATION, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Align:", self.data_options["bar"]["align"], ALIGN, row=row, col=col)
            elif mode == "pie":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Explode:", self.data_options["pie"]["explode"], row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Autopct:", self.data_options["pie"]["autopct"], row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Start angle:", self.data_options["pie"]["startangle"], row=row, col=col)
            elif mode == "boxplot":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["boxplot"]["y"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Vertical:", self.data_options["boxplot"]["vert"], TF, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Patch artist:", self.data_options["boxplot"]["patch_artist"], TF, row=row, col=col)
            elif mode == "violin":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["violin"]["y"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Show means:", self.data_options["violin"]["showmeans"], TF, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Show extrema:", self.data_options["violin"]["showextrema"], TF, row=row, col=col)
            elif mode == "heatmap":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["heatmap"]["y"], column, row=row, col=col)
                _, col = ui.add_color(specific_frame, self.data_options["heatmap"]["cmap"], row=row, col=col, tooltip="Color")
                _, col = ui.add_label_optionmenu(specific_frame, "Interpolation:", self.data_options["heatmap"]["interpolation"], ["nearest", "bilinear", "bicubic"], row=row, col=col)
            elif mode == "contour":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["contour"]["y"], column, row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Levels:", self.data_options["contour"]["levels"], row=row, col=col)
                _, col = ui.add_color(specific_frame, self.data_options["contour"]["cmap"], row=row, col=col, tooltip="Color")
                _, col = ui.add_label_entry(specific_frame, "X min:", self.data_options["common"]["x_min"], row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "X max:", self.data_options["common"]["x_max"], row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Y min:", self.data_options["common"]["y_min"], row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Y max:", self.data_options["common"]["y_max"], row=row, col=col)
            elif mode == "quiver":  
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["quiver"]["y"], column, row=row, col=col)
                _, col = ui.add_label_entry(specific_frame, "Scale:", self.data_options["quiver"]["scale"], row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Scale units:", self.data_options["quiver"]["scale_units"], ["xy", "width", "height", "dots"], row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Angles:", self.data_options["quiver"]["angles"], ["xy", "uv", "degrees"], row=row, col=col)
            elif mode == "polar":
                _, col = ui.add_label_optionmenu(specific_frame, "Theta:", self.data_options["polar"]["theta"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "R:", self.data_options["polar"]["r"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Theta units:", self.data_options["polar"]["theta_units"], ["radians", "degrees"], row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "R units:", self.data_options["polar"]["r_units"], ["linear", "logarithmic"], row=row, col=col)
            elif mode == "stack":
                _, col = ui.add_label_optionmenu(specific_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Y:", self.data_options["stack"]["y"], column, row=row, col=col)
                _, col = ui.add_label_optionmenu(specific_frame, "Stacked:", self.data_options["stack"]["stacked"], TF, row=row, col=col)
        # Bind refresh to mode change
        self.data_options["plot_select"].trace_add("write", refresh_options)

        # Initially show options for "plot"
        refresh_options()
       
    def toggle_regression(self, specific_frame, toggle_button):
        if hasattr(self, "reg_frame") and self.reg_frame.winfo_exists():
            self.reg_frame.destroy()
            toggle_button.config(text="Esegui Fit")
            self.data_options['fit']['plot_reg'].set("No")
        else:
            self.reg_frame = tk.Frame(specific_frame, bg="lightgreen",borderwidth=1, relief=tk.SUNKEN)
            self.reg_frame.grid(row=2, column=0, columnspan=6, sticky="w")
            RegressionApp(self.reg_frame, self.data_options, self.data_options["file path"])
            toggle_button.config(text="Rimuovi fit")


    def plot_config(self,specific_frame,column):
        container = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        container.grid(row=0, column=0, sticky="ew")
        canvas = tk.Canvas(container, bg="lightblue", height=dim.s(266), width=dim.s(1000))
        canvas.grid(row=0, column=0, sticky="ew")
        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        canvas.configure(xscrollcommand=h_scrollbar.set)
        
        color = "lightblue"
        axis_frame = tk.Frame(canvas, bg=color)
        canvas.create_window((0, 0), window=axis_frame, anchor="nw")
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        axis_frame.bind("<Configure>", update_scrollregion)
        container.grid_columnconfigure(0, weight=1)
        row, col = 1, 0

        _, col = ui.add_label_entry(axis_frame, "Label:", self.data_options["common"]["label"], entry_width=60, row=row, col=col, columnspan=6, tooltip="Etichetta descrittiva per la legenda", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(axis_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col, label_font=("Arial", 10, "bold"), tooltip="Seleziona la colonna per l'asse X", colorbg=color)
        _, col = ui.add_label_optionmenu(axis_frame, "X error:", self.data_options["common"]["x_err"], column + ["None"], row=row, col=col, tooltip="Seleziona la colonna per l'errore su X", colorbg=color)
        _, col = ui.add_label_optionmenu(axis_frame, "X2:", self.data_options["common"]["x2"], column + ["None"], row=row, col=col, tooltip="Seleziona un'ulteriore colonna per X", colorbg=color)
        _, col = ui.add_label(axis_frame, "X min-max:", row=row, col=col, tooltip="Limiti asse X (vuoto per auto)", colorbg=color)
        _, col = ui.add_entry(axis_frame, self.data_options["common"]["x_min"], entry_width=8, row=row, col=col, tooltip="Valore minimo X")
        _, col = ui.add_label(axis_frame, "-", row=row, col=col, colorbg=color)
        _, col = ui.add_entry(axis_frame, self.data_options["common"]["x_max"], entry_width=8, row=row, col=col, tooltip="Valore massimo X")
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, "x-Fun:", self.data_options["common"]["x_function"], entry_width=35, row=row, col=col, columnspan=4, tooltip="Funzione di trasformazione per X (es: x*10)", colorbg=color)
        col += 3
        _, col = ui.add_label_entry(axis_frame, "x-Par:", self.data_options["common"]["x_parameters"], entry_width=35, row=row, col=col, columnspan=4, tooltip="Parameters: inserire\n parametri nel formato\npar1=value1,par2=value2,...", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(axis_frame, "Y:", self.data_options["plot"]["y"], column, row=row, col=col, label_font=("Arial", 10, "bold"), tooltip="Seleziona la colonna per l'asse Y", colorbg=color)
        _, col = ui.add_label_optionmenu(axis_frame, "Y error:", self.data_options["plot"]["y_err"], column + ["None"], row=row, col=col, tooltip="Seleziona la colonna per l'errore su Y", colorbg=color)
        _, col = ui.add_label_optionmenu(axis_frame, "Y2:", self.data_options["plot"]["y2"], column + ["None"], row=row, col=col, tooltip="Seleziona un'ulteriore colonna per Y", colorbg=color)
        _, col = ui.add_label(axis_frame, "Y min-max:", row=row, col=col, tooltip="Limiti asse Y (vuoto per auto)", colorbg=color)
        _, col = ui.add_entry(axis_frame, self.data_options["plot"]["y_min"], entry_width=8, row=row, col=col, tooltip="Valore minimo Y")
        _, col = ui.add_label(axis_frame, "-", row=row, col=col, colorbg=color)
        _, col = ui.add_entry(axis_frame, self.data_options["plot"]["y_max"], entry_width=8, row=row, col=col, tooltip="Valore massimo Y")
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, "y-Fun:", self.data_options["common"]["y_function"], entry_width=35, row=row, col=col, columnspan=4, tooltip="Funzione di trasformazione per Y (es: y/2)", colorbg=color)
        col += 3
        _, col = ui.add_label_entry(axis_frame, "y-Par:", self.data_options["common"]["y_parameters"], entry_width=35, row=row, col=col, columnspan=4, tooltip="Parameters: inserire\n parametri nel formato\npar1=value1,par2=value2,...", colorbg=color)
        
        
        options_frame = tk.Frame(specific_frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        options_frame.grid(row=0, column=1, sticky="ew")
        
        color_frame = tk.Frame(options_frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        color_frame.grid(row=0, column=0)
        _, col = ui.add_color(color_frame, self.data_options["common"]["color"], row=0, col=0, tooltip="Colore principale della serie")
        _, col = ui.add_scale(color_frame, self.data_options["common"]["alpha"], from_=0, to=1, resolution=0.05, row=1, col=0, tooltip="Trasparenza (0=invisibile, 1=opaco)", colorbg=color)
        _, col = ui.add_color(color_frame, self.data_options["plot"]["mfcolor"], row=0, col=1, tooltip="Colore interno del Marker")
        _, col = ui.add_optionmenu(color_frame, self.data_options["plot"]["mfc"], YN, row=1, col=1, tooltip="Attiva/Disattiva riempimento marker", colorbg=color)
        
        marker_frame = tk.Frame(options_frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        marker_frame.grid(row=0, column=1)
        _, col = ui.add_optionmenu(marker_frame, self.data_options["plot"]["marker"], MARKER, row=0, col=0, tooltip="Scegli lo stile del marker", colorbg=color)
        _, col = ui.add_scale(marker_frame, self.data_options["plot"]["ms"], from_=0, to=10, resolution=0.1, row=1, col=0, tooltip="Dimensione del marker", colorbg=color)
        
        line_frame = tk.Frame(options_frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        line_frame.grid(row=0, column=2)
        _, col = ui.add_optionmenu(line_frame, self.data_options["plot"]["line"], LINE, row=0, col=0, tooltip="Stile della linea", colorbg=color)
        _, col = ui.add_scale(line_frame, self.data_options["plot"]["lw"], from_=0, to=3, resolution=0.1, row=1, col=0, tooltip="Spessore della linea", colorbg=color)
        
        error_frame = tk.Frame(options_frame, bg=color, borderwidth=1, relief=tk.SUNKEN)
        error_frame.grid(row=2, column=0, columnspan=3)
        row = 0; col = 0
        _, col = ui.add_color(error_frame, self.data_options['plot']["errorbar"]["ecolor"], row=row, col=col, tooltip="Colore delle barre d'errore")
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["elinewidth"], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Spessore linea barre d'errore", colorbg=color)
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["capsize"], from_=0, to=10, resolution=0.5, row=row, col=col, tooltip="Dimensione dei terminali (cap)", colorbg=color)
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["capthick"], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Spessore dei terminali (cap)", colorbg=color)
        
        filter_container = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        filter_container.grid(row=0, column=2, sticky="ew")
        filter_canvas = tk.Canvas(filter_container, bg="lightblue", height=dim.s(250), width=dim.s(480))
        filter_canvas.grid(row=0, column=0, sticky="ew")
        filter_scrollbar = tk.Scrollbar(filter_container, orient="horizontal", command=filter_canvas.xview)
        filter_scrollbar.grid(row=1, column=0, sticky="ew")
        filter_canvas.configure(xscrollcommand=filter_scrollbar.set)
        
        color = "lightblue"
        # --- DEFINIZIONE TOOLTIP ---
        tooltip_rules = (
            "MODALITÀ STANDARD (Compare = None):\n"
            "  5       (uguale a 5)\n"
            "  >10     (maggiore di 10)\n"
            "  <=5.5   (minore o uguale)\n"
            "  !=0     (diverso da 0)\n"
            "  >0,<10  (compreso tra 0 e 10)\n\n"
            "MODALITÀ CONFRONTO (Compare selezionato):\n"
            "  <, >, =      (Confronto diretto: x < y)\n"
            "  x > y + 5    (Espressioni con x e y)\n"
            "  x < np.log(y)(Funzioni NumPy)\n"
            "  * x = colonna filtro, y = colonna compare"
        )
        filter_frame = tk.Frame(filter_canvas, bg=color)
        filter_canvas.create_window((0, 0), window=filter_frame, anchor="nw")
        def update_scrollregion(event):
            filter_canvas.configure(scrollregion=filter_canvas.bbox("all"))
        filter_frame.bind("<Configure>", update_scrollregion)
        filter_container.grid_columnconfigure(0, weight=0)
        row, col = 0, 0
        _, col = ui.add_label_optionmenu(filter_frame, "Filtro 1)", self.data_options["common"]["col_filter1"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
        _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter1"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
        _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter1"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da comparare,\n altrimenti lascia None", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(filter_frame, "Filtro 2)", self.data_options["common"]["col_filter2"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
        _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter2"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
        _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter2"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da comparare,\n altrimenti lascia None", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(filter_frame, "Filtro 3)", self.data_options["common"]["col_filter3"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
        _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter3"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
        _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter3"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da comparare,\n altrimenti lascia None", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(filter_frame, "Filtro 4)", self.data_options["common"]["col_filter4"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
        _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter4"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
        _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter4"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da comparare,\n altrimenti lascia None", colorbg=color)
        


    def hist_config(self,specific_frame,column):
            colorbg = "lightgreen"

            container = tk.Frame(specific_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            container.grid(row=0, column=0, sticky="ew")
            canvas = tk.Canvas(container, bg=colorbg, height=dim.s(200), width=dim.s(750))
            canvas.grid(row=0, column=0, sticky="ew")
            h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
            h_scrollbar.grid(row=1, column=0, sticky="ew")
            canvas.configure(xscrollcommand=h_scrollbar.set)
            
            color = "lightgreen"
            main_frame = tk.Frame(canvas, bg=color)
            canvas.create_window((0, 0), window=main_frame, anchor="nw")
            def update_scrollregion(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            main_frame.bind("<Configure>", update_scrollregion)
            container.grid_columnconfigure(0, weight=1)
            row, col = 0, 0
            _, col = ui.add_label_entry(main_frame, "Label:", self.data_options["common"]["label"], entry_width=60, columnspan=8, row=row, col=col, tooltip="Etichetta per la legenda", colorbg=colorbg)
            row += 1; col =0
            _, col = ui.add_label_optionmenu(main_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col, label_font=("Arial", 10, "bold"), tooltip="Seleziona la colonna dati principale (X)", colorbg=colorbg)
            _, col = ui.add_label_optionmenu(main_frame, "X2:", self.data_options["common"]["x2"], column, row=row, col=col, tooltip="Seleziona una seconda colonna dati (opzionale)", colorbg=colorbg)
            _, col = ui.add_label_entry(main_frame, "min-max:", self.data_options["common"]["x_min"], entry_width=8, row=row, col=col, tooltip="Valore minimo range X", colorbg=colorbg)
            _, col = ui.add_label_entry(main_frame, "-", self.data_options["common"]["x_max"], entry_width=8, row=row, col=col, tooltip="Valore massimo range X", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_entry(main_frame, "Fun:", self.data_options["common"]["x_function"], entry_width=60, row=row, col=col, columnspan=8, tooltip="Funzione da applicare ai dati (es. np.log(x))", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_entry(main_frame, "Par:", self.data_options["common"]["x_parameters"], entry_width=60, row=row, col=col, columnspan=8, tooltip="Parametri aggiuntivi per la funzione", colorbg=colorbg)
            
            color_frame = tk.Frame(specific_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            color_frame.grid(row=1,column=0)
            ui.add_color(color_frame, self.data_options["common"]["color"], row=0, col=0, tooltip="Colore di riempimento istogramma")
            ui.add_scale(color_frame, self.data_options["common"]["alpha"], from_=0, to=1, resolution=0.05, row=0, col=1, tooltip="Trasparenza riempimento", colorbg=colorbg)
            contour_frame = tk.Frame(color_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            contour_frame.grid(row=0,column=2)
            ui.add_color(contour_frame, self.data_options["hist"]["contour_color"], row=0, col=0, tooltip="Colore del bordo (contour)")
            ui.add_scale(contour_frame, self.data_options["hist"]["contour_alpha"], from_=0, to=1, resolution=0.05, row=0, col=1, tooltip="Trasparenza del bordo", colorbg=colorbg)
            ui.add_optionmenu(contour_frame, self.data_options["hist"]["contour_line"], LINE, row=0, col=2, tooltip="Stile linea del bordo", colorbg=colorbg)
            ui.add_scale(contour_frame, self.data_options["hist"]["contour_width"], from_=0, to=3, resolution=0.1, row=0, col=3, tooltip="Spessore linea del bordo", colorbg=colorbg)
            
            
            option_frame = tk.Frame(specific_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            option_frame.grid(row=0,column=1, rowspan=2, sticky="w")
            row, col = 0, 0
            _, col = ui.add_label_optionmenu(option_frame, "Type:", self.data_options["hist"]["histtype"], HISTTYPE, row=row, col=col, tooltip="Tipo di istogramma (bar, step, etc.)", colorbg=colorbg)
            _, col = ui.add_label_entry(option_frame, "Bottom:", self.data_options["hist"]["bottom"], entry_width=8, row=row, col=col, tooltip="Valore di partenza asse Y (baseline)", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_entry(option_frame, "Bins:", self.data_options["hist"]["bins"], entry_width=8, row=row, col=col, tooltip="Numero di intervalli (bins)", colorbg=colorbg)
            _, col = ui.add_label(option_frame, "width:", row=row, col=col, tooltip="Larghezza relativa barre", colorbg=colorbg)
            _, col = ui.add_scale(option_frame, self.data_options["hist"]["rwidth"], from_=0, to=1, resolution=0.05, row=row, col=col, tooltip="Larghezza relativa barre (rwidth)", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(option_frame, "Align:", self.data_options["hist"]["align"], ALIGN, row=row, col=col, tooltip="Allineamento barre rispetto ai tick", colorbg=colorbg)
            _, col = ui.add_label_optionmenu(option_frame, "Orientation:", self.data_options["hist"]["orientation"], ORIENTATION, row=row, col=col, tooltip="Orientamento (verticale/orizzontale)", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(option_frame, "Density:", self.data_options["hist"]["density"], TF, row=row, col=col, tooltip="Normalizza area a 1 (Densità)", colorbg=colorbg)
            _, col = ui.add_label_optionmenu(option_frame, "Cumulative:", self.data_options["hist"]["cumulative"], TF, row=row, col=col, tooltip="Istogramma cumulativo", colorbg=colorbg)
                    
            
            tick_frame = tk.Frame(specific_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            tick_frame.grid(row=0,column=2, rowspan=2, sticky="w")
            row, col = 0, 0
            _, col = ui.add_label_optionmenu(tick_frame, "Axis:", self.data_options["hist"]["tick_par"]["axis"], AXIS, row=row, col=col,colspan=4, tooltip="Applica tick all'asse X, Y o entrambi", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(tick_frame, "Direction:", self.data_options["hist"]["tick_par"]["direction"], ['inout', 'out', 'in'],row=row, col=col,colspan=4, tooltip="Direzione dei tick (interno/esterno)", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_color(tick_frame, self.data_options["hist"]["tick_par"]["labelcolor"], row=row, col=col, tooltip="Colore delle etichette (numeri)")
            _, col = ui.add_label_entry(tick_frame, "Length:", self.data_options["hist"]["tick_par"]["length"], entry_width=6, row=row, col=col, tooltip="Lunghezza delle stanghette tick", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_color(tick_frame, self.data_options["hist"]["tick_par"]["color"], row=row, col=col, tooltip="Colore delle stanghette tick")
            _, col = ui.add_label_entry(tick_frame, "Width:", self.data_options["hist"]["tick_par"]["width"], entry_width=6, row=row, col=col, tooltip="Spessore delle stanghette tick", colorbg=colorbg)
            row += 1; col = 0
            _, col = ui.add_label_entry(tick_frame, "Size/Pad:", self.data_options["hist"]["tick_par"]["labelsize"], entry_width=4, row=row, col=col, tooltip="Dimensione font etichette", colorbg=colorbg)
            _, col = ui.add_entry(tick_frame, self.data_options["hist"]["tick_par"]["pad"], entry_width=4, row=row, col=col, tooltip="Distanza etichetta dall'asse (pad)")
            
            filter_container = tk.Frame(specific_frame, bg=colorbg,borderwidth=1, relief=tk.SUNKEN)
            filter_container.grid(row=0, column=3, rowspan=2, sticky="ew")
            filter_canvas = tk.Canvas(filter_container, bg=colorbg, height=dim.s(250), width=dim.s(480))
            filter_canvas.grid(row=0, column=0, sticky="ew")
            filter_scrollbar = tk.Scrollbar(filter_container, orient="horizontal", command=filter_canvas.xview)
            filter_scrollbar.grid(row=1, column=0, sticky="ew")
            filter_canvas.configure(xscrollcommand=filter_scrollbar.set)
            
            color = "lightgreen"
            # --- DEFINIZIONE TOOLTIP ---
            tooltip_rules = (
                "MODALITÀ STANDARD (Compare = None):\n"
                "  5       (uguale a 5)\n"
                "  >10     (maggiore di 10)\n"
                "  <=5.5   (minore o uguale)\n"
                "  !=0     (diverso da 0)\n"
                "  >0,<10  (compreso tra 0 e 10)\n\n"
                "MODALITÀ CONFRONTO (Compare selezionato):\n"
                "  <, >, =      (Confronto diretto: x < y)\n"
                "  x > y + 5    (Espressioni con x e y)\n"
                "  x < np.log(y)(Funzioni NumPy)\n"
                "  * x = colonna filtro, y = colonna compare"
            )
            filter_frame = tk.Frame(filter_canvas, bg=color)
            filter_canvas.create_window((0, 0), window=filter_frame, anchor="nw")
            def update_scrollregion(event):
                filter_canvas.configure(scrollregion=filter_canvas.bbox("all"))
            filter_frame.bind("<Configure>", update_scrollregion)
            filter_container.grid_columnconfigure(0, weight=0)
            row, col = 0, 0
            _, col = ui.add_label_optionmenu(filter_frame, "Filtro 1)", self.data_options["common"]["col_filter1"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
            _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter1"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
            _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter1"], column + ["None"], row=row, col=col, tooltip="Colonna di confronto (y) per il filtro", colorbg=color)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(filter_frame, "Filtro 2)", self.data_options["common"]["col_filter2"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
            _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter2"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
            _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter2"], column + ["None"], row=row, col=col, tooltip="Colonna di confronto (y) per il filtro", colorbg=color)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(filter_frame, "Filtro 3)", self.data_options["common"]["col_filter3"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
            _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter3"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
            _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter3"], column + ["None"], row=row, col=col, tooltip="Colonna di confronto (y) per il filtro", colorbg=color)
            row += 1; col = 0
            _, col = ui.add_label_optionmenu(filter_frame, "Filtro 4)", self.data_options["common"]["col_filter4"], column + ["None"], row=row, col=col, tooltip="Seleziona una colonna da filtrare", colorbg=color)
            _, col = ui.add_entry(filter_frame, self.data_options["common"]["filter4"], entry_width=8, row=row, col=col, tooltip=tooltip_rules)
            _, col = ui.add_optionmenu(filter_frame, self.data_options["common"]["col_compare_filter4"], column + ["None"], row=row, col=col, tooltip="Colonna di confronto (y) per il filtro", colorbg=color)
        
    def toggle_frame(self, specific_frame):
        if self.expanded:
            # Compress (hide specific_frame)
            specific_frame.grid_remove()
            self.toggle_button.config(text="▶")  # right arrow
        else:
            # Expand (show specific_frame)
            specific_frame.grid()
            self.toggle_button.config(text="▼")  # down arrow
        self.expanded = not self.expanded
        
    def remove_data(self, frame, data_id, all_data_id, data_options):
        #Removes the current dataset from the GUI and resets the associated options.
        # Checks that the current dataset matches the id
        if data_options.get("data_id") == data_id:
            # Resets all options
            data_options = None  # or {} if you prefer to keep it as an empty dictionary
        # Destroys the frame associated with the dataset
        frame.destroy()
        if data_id in all_data_id:
            all_data_id.remove(data_id)
        # Updates the GUI if the frame was inside a scrollable container
        if hasattr(self.root, "update_idletasks"):
            self.root.update_idletasks()
        
class InsertFunction:
    def __init__(self, root, inset_counter, function_id, function_options, all_function_id, upload):
        self.root = root
        self.upload = upload
        
        # Options dictionary
        self.function_options = {
            "inset": inset_counter,
            "function_select": tk.StringVar(value="function"),
            "show/hide": tk.StringVar(value="1"),
            "function" : {
                "function": tk.StringVar(value=""),
                "parameters": tk.StringVar(value=""),
                "x min": tk.StringVar(value=""),
                "x max": tk.StringVar(value=""),
                "label": tk.StringVar(),
                "line": tk.StringVar(value="solid"),
                "lw": tk.StringVar(value="1"),
                "color": tk.StringVar(value="black"),
                "alpha": tk.StringVar(value="1")
            },
            "axhline" : {
                "y": tk.StringVar(value=""),
                "label": tk.StringVar(),
                "line": tk.StringVar(value="solid"),
                "lw": tk.StringVar(value="1"),
                "color": tk.StringVar(value="black"),
                "alpha": tk.StringVar(value="1")
            },
            "axvline" : {
                "x": tk.StringVar(value=""),
                "label": tk.StringVar(),
                "line": tk.StringVar(value="solid"),
                "lw": tk.StringVar(value="1"),
                "color": tk.StringVar(value="black"),
                "alpha": tk.StringVar(value="1")
            },
            "axhspan": {
                "y1": tk.StringVar(value=""),
                "y2": tk.StringVar(value=""),
                "label": tk.StringVar(value=""),
                "facecolor": tk.StringVar(value=COLOR[0]),
                "edgecolor": tk.StringVar(value=COLOR[0]),
                "alpha": tk.StringVar(value="1")
            },
            "axvspan": {
                "x1": tk.StringVar(value=""),
                "x2": tk.StringVar(value=""),
                "label": tk.StringVar(value=""),
                "facecolor": tk.StringVar(value=COLOR[0]),
                "edgecolor": tk.StringVar(value=COLOR[0]),
                "alpha": tk.StringVar(value="1")
            },
            # Rettangolo (patch Rectangle)
            "patch": {
                "x1": tk.StringVar(value=""),
                "x2": tk.StringVar(value=""),
                "y1": tk.StringVar(value=""),
                "y2": tk.StringVar(value=""),
                "label": tk.StringVar(value=""),
                "line": tk.StringVar(value="solid"),   # linestyle (stroke style)
                "lw": tk.StringVar(value="1"),         # linewidth
                "facecolor": tk.StringVar(value=COLOR[0]), # used for BOTH edge and face
                "edgecolor": tk.StringVar(value=COLOR[0]), # used for BOTH edge and face
                "alpha": tk.StringVar(value="1")       # transparency
            }
        }
    
        self.options(function_options, function_id, all_function_id)
        function_options[function_id] = self.function_options

    def options(self,function_options, function_id, all_function_id):
        # Main frame
        color = "lightgreen"
        frame = tk.Frame(self.root, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
       
        if self.upload:
            self.function_options = function_options[function_id]
        # --- Row 1: Info file ---
        
        trash_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "cestino.png")).subsample(20, 20)
        # Create "Remove" button with trash icon
        tk.Button(frame, image=trash_icon, command=lambda: self.remove_function(frame, function_id, all_function_id, function_options)).grid(row=0, column=0, padx=dim.s(5), pady=dim.s(5), sticky="w")
        if not hasattr(self, 'trash_icons'):
            self.trash_icons = []
        self.trash_icons.append(trash_icon)
        ui.add_checkbutton(frame, "Show function", self.function_options["show/hide"], row=0, col=2, label_font=dim.label_font(14), tooltip="Mostra/Nascondi funzione", colorbg="lightgreen")
        ui.add_label_optionmenu(frame, "Mode:", self.function_options["function_select"], FUNCTION, row=0, col=3, colorbg=color)

        # Arrow button (if you use it)
                # Variable for expansion state
        self.expanded = True  

        # Arrow button (initially "▼")
        self.toggle_button = tk.Button(
            frame, text="▼", width=2, command=lambda: self.toggle_frame(specific_frame)
        )
        self.toggle_button.grid(row=0, column=5, padx=dim.s(5), pady=dim.s(5), sticky="e")


        # ⬅️ GIVE WEIGHT TO COLUMN 1 (the one with the label)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)  # expands to fill
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=0)

        # --- Frame for specific options: takes full width
        specific_frame = tk.Frame(frame, bg=color)
        specific_frame.grid(row=1, column=0, columnspan=6, sticky="ew")
        specific_frame.grid_columnconfigure(0, weight=1)  # to stretch internally, if necessary

    
        # Function to update specific options
        def refresh_options(*args):
            # Clear previous specific widgets
            for widget in specific_frame.grid_slaves():
                widget.destroy()

            mode = self.function_options["function_select"].get()

            if mode == "function":
                self.function_config(specific_frame)
            if mode == "h-line":
                self.axhline_config(specific_frame)
            if mode == "v-line":
                self.axvline_config(specific_frame)
            if mode == "h-span":
                self.axhspan_config(specific_frame)
            if mode == "v-span":
                self.axvspan_config(specific_frame)
            if mode == "patch":
                self.patch_config(specific_frame)
        self.function_options["function_select"].trace_add("write", refresh_options)

        refresh_options()
        
    def function_config(self, frame):        
        color = "lightgreen"
        func_frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        func_frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        fun_opt = self.function_options["function"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(func_frame, "Function:", fun_opt["function"], entry_width=45, entry_font=("Arial", 13), row=0, col=0, columnspan=5, colorbg=color)
        _, col = ui.add_label_entry(func_frame, "Parameters:", fun_opt["parameters"], entry_width=90, row=1, col=0, columnspan=5, tooltip="Parameters: inserire\n parametri nel formato\npar1=value1,par2=value2,...", colorbg=color)
        row = 2; col = 0
        _, col = ui.add_label_entry(func_frame, "Label:", fun_opt["label"], entry_width=50, row=row, col=0, colorbg=color)
        _, col = ui.add_label(func_frame, "X min-max",row=row, col=col, colorbg=color)
        _, col = ui.add_entry(func_frame, fun_opt["x min"], entry_width=8, row=row, col=col)
        _, col = ui.add_label(func_frame, "-",row=row, col=col, colorbg=color)
        _, col = ui.add_entry(func_frame, fun_opt["x max"], entry_width=8, row=row, col=col)

        opt_frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        opt_frame.grid(row = 0, column = 2, padx=dim.s(5), pady=dim.s(5))
        row = 0; col = 0
        _, col = ui.add_color(opt_frame, fun_opt["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(opt_frame, fun_opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_optionmenu(opt_frame, fun_opt["line"], LINE, row=row, col=col, tooltip="Line", colorbg=color)
        _, col = ui.add_scale(opt_frame, fun_opt["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line Width", colorbg=color)

    def axhline_config(self, frame):
        color = "lightgreen"        
        frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        opt = self.function_options["axhline"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(frame, "Label:", opt["label"], entry_width=45, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "y:", opt["y"], entry_width=10, row=row, col=col, colorbg=color)
        
        _, col = ui.add_optionmenu(frame, opt["line"], LINE, row=row, col=col, tooltip="Line", colorbg=color)
        _, col = ui.add_scale(frame, opt["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line Width", colorbg=color)

        _, col = ui.add_color(frame, opt["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
        
    def axvline_config(self, frame):
        color = "lightgreen"
        frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        opt = self.function_options["axvline"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(frame, "Label:", opt["label"], entry_width=45, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "x:", opt["x"], entry_width=10, row=row, col=col, colorbg=color)
        
        _, col = ui.add_optionmenu(frame, opt["line"], LINE, row=row, col=col, tooltip="Line", colorbg=color)
        _, col = ui.add_scale(frame, opt["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line Width", colorbg=color)

        _, col = ui.add_color(frame, opt["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
        
        
    def axhspan_config(self, frame):        
        color = "lightgreen"
        frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        opt = self.function_options["axhspan"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(frame, "Label:", opt["label"], entry_width=45, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "y:", opt["y1"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "-", opt["y2"], entry_width=10, row=row, col=col, colorbg=color)
        
        _, col = ui.add_color(frame, opt["facecolor"], row=row, col=col, tooltip="Color")
        _, col = ui.add_color(frame, opt["edgecolor"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
    
    def axvspan_config(self, frame):        
        color = "lightgreen"
        frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        opt = self.function_options["axvspan"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(frame, "Label:", opt["label"], entry_width=45, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "x:", opt["x1"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "-", opt["x2"], entry_width=10, row=row, col=col, colorbg=color)
        
        _, col = ui.add_color(frame, opt["facecolor"], row=row, col=col, tooltip="Color")
        _, col = ui.add_color(frame, opt["edgecolor"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
        
    def patch_config(self, frame):     
        color = "lightgreen"   
        frame = tk.Frame(frame, bg=color, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        
        opt = self.function_options["patch"]
        
        col = 0
        row = 0
        
        _, col = ui.add_label_entry(frame, "Label:", opt["label"], entry_width=50, row=row, col=col, columnspan=7, colorbg=color)
        col += 7
        _, col = ui.add_optionmenu(frame, opt["line"], LINE, row=row, col=col, tooltip="Line", colorbg=color)
        _, col = ui.add_scale(frame, opt["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line Width", colorbg=color)

        col = 0
        row = 1
        _, col = ui.add_label_entry(frame, "x:", opt["x1"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "-", opt["x2"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "y:", opt["y1"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(frame, "-", opt["y2"], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_color(frame, opt["facecolor"], row=row, col=col, tooltip="Face color")
        _, col = ui.add_color(frame, opt["edgecolor"], row=row, col=col, tooltip="Edge color")
        _, col = ui.add_scale(frame, opt["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", colorbg=color)
        
    def toggle_frame(self, specific_frame):
        if self.expanded:
            # Compress (hide specific_frame)
            specific_frame.grid_remove()
            self.toggle_button.config(text="▶")  # right arrow
        else:
            # Expand (show specific_frame)
            specific_frame.grid()
            self.toggle_button.config(text="▼")  # down arrow
        self.expanded = not self.expanded

    def remove_function(self, frame, function_id, all_function_id, function_options):
        if function_options.get("function_id") == function_id:
            function_options = None  
        frame.destroy()
        if function_id in all_function_id:
            all_function_id.remove(function_id)
        if hasattr(self.root, "update_idletasks"):
            self.root.update_idletasks()
            
class InsetOptions:
    def __init__(self, root, inset_counter,inset_id,inset_options,all_inset_id,MainPage, upload=False):
        self.root = root
        self.main_page = MainPage
        self.upload = upload

        # Options dictionary
        self.inset_opt = {
            'inset': inset_counter,
            'inset_id': inset_id,
            "show/hide": tk.StringVar(value="1"),
            'title': tk.StringVar(value=None),
            'x_label': tk.StringVar(value=None), 
            'y_label': tk.StringVar(value=None),
            'x_dim': tk.StringVar(value=8), 
            'y_dim': tk.StringVar(value=6), 
            'x_min': tk.StringVar(value=None), 
            'x_max': tk.StringVar(value=None),
            'y_min': tk.StringVar(value=None), 
            'y_max': tk.StringVar(value=None),
            'log': tk.StringVar(value="None"),
            'x_thick': tk.StringVar(value=None),
            'y_thick': tk.StringVar(value=None),
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
            'position': {
                'left': tk.StringVar(value="0.5"), 
                'bottom': tk.StringVar(value="0.5"), 
                'width': tk.StringVar(value="0.4"), 
                'height': tk.StringVar(value="0.4")
            },
            'legend': {
                'legend': tk.StringVar(value="No"), 
                'legend_position': tk.StringVar(value=LEGEND[0]), 
                'legend_size': tk.StringVar(value="10")
            },
            'font': {
                "title_size": tk.StringVar(value="10"),         # Title size
                "label_size": tk.StringVar(value="10"),        # X axis label size
                "xaxis_size": tk.StringVar(value="10"),        # X axis tick label size
                "yaxis_size": tk.StringVar(value="10"),        # Y axis tick label size
                "color": tk.StringVar(value=COLOR[5])            # Text color
            },
            'sci': {
                'style': tk.StringVar(value='plain'),
                'axis': tk.StringVar(value='both'),
                'min_scilimits': tk.StringVar(value=0),
                'max_scilimits': tk.StringVar(value=0)
            },
        }
        self.options(inset_id, inset_options, all_inset_id)

    def options(self, inset_id, inset_options, all_inset_id):
        self.frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
        self.frame.pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
        
        if self.upload:
            self.inset_opt = inset_options[inset_id]

        # Button to remove inset
        trash_icon = tk.PhotoImage(file=os.path.join(BASE_DIR, "cestino.png")).subsample(20, 20)
        tk.Button(self.frame, image=trash_icon, command=lambda: self.remove_inset(inset_id, inset_options, all_inset_id)).grid(row=0, column=0, padx=dim.s(5), pady=dim.s(5))
        if not hasattr(self, 'trash_icons'):
            self.trash_icons = []
        self.trash_icons.append(trash_icon)
        
        color = "lightblue"
        main_frame = tk.Frame(self.frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        main_frame.grid(row=0,column=1)

        axis_frame = tk.Frame(main_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        axis_frame.grid(row=0,column=0,columnspan=2)
        row = 0; col = 0
        _, col = ui.add_label_entry(axis_frame, "Title:", self.inset_opt['title'], entry_width= 80, row=row, col=col, columnspan=7, colorbg=color)
        col += 6
        _, col = ui.add_label_optionmenu(axis_frame, "Log:", self.inset_opt['log'], LOG, row=row, col=col, colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, 'X label', self.inset_opt['x_label'], entry_width=40, row=row, col=col, columnspan=3, colorbg=color)
        col += 2
        _, col = ui.add_label_entry(axis_frame, 'X min/max', self.inset_opt['x_min'], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(axis_frame, '-', self.inset_opt['x_max'], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(axis_frame, 'x thick', self.inset_opt['x_thick'], entry_width=8, row=row, col=col, colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, 'Y label', self.inset_opt['y_label'], entry_width=40, row=row, col=col, colorbg=color)
        col += 2
        _, col = ui.add_label_entry(axis_frame, 'Y min/max', self.inset_opt['y_min'], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(axis_frame, '-', self.inset_opt['y_max'], entry_width=10, row=row, col=col, colorbg=color)
        _, col = ui.add_label_entry(axis_frame, 'y thick', self.inset_opt['y_thick'], entry_width=8, row=row, col=col, colorbg=color)
        
        font_frame = tk.Frame(main_frame,borderwidth=1, relief=tk.SUNKEN)
        font_frame.grid(row=1,column=0)
        row = 0; col = 0
        _, col = ui.add_label_entry(font_frame, "Title:", self.inset_opt['font']['title_size'], entry_width=4, row=row, col=col, tooltip="Title size")
        _,col = ui.add_label(font_frame, "", row=row, col=col)  # Spacer
        _, col = ui.add_color(font_frame, self.inset_opt['font']["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_label_entry(font_frame, "Label size:", self.inset_opt['font']['label_size'], entry_width=4, row=row, col=col, tooltip="Label size")
        _, col = ui.add_label_entry(font_frame, "X/Y ax:", self.inset_opt['font']['xaxis_size'], entry_width=4, row=row, col=col, tooltip="X thick size")
        _, col = ui.add_label_entry(font_frame, "-", self.inset_opt['font']['yaxis_size'], entry_width=4, row=row, col=col, tooltip="Y thick size")
        
        legend_frame = tk.Frame(main_frame,borderwidth=1, relief=tk.SUNKEN)
        legend_frame.grid(row=1,column=1)
        col = 0; row = 0
        _, col = ui.add_label(legend_frame, "Legend\noptions:", row=row, col=col)
        _, col = ui.add_optionmenu(legend_frame, self.inset_opt['legend']['legend'], YN, row=row, col=col, tooltip="Show legend")
        _, col = ui.add_entry(legend_frame, self.inset_opt['legend']['legend_size'], entry_width=6, row=row, col=col, tooltip="Size")
        _, col = ui.add_optionmenu(legend_frame, self.inset_opt['legend']['legend_position'], LEGEND, row=row, col=col, tooltip="Position")
        
        
        color ="lightgreen"
        position_frame = tk.Frame(self.frame,borderwidth=1, bg=color, relief=tk.SUNKEN)
        position_frame.grid(row=0,column=2)
        row = 0; col = 0
        ui.add_checkbutton(position_frame, "Show inset", self.inset_opt["show/hide"], row=0, col=0, colspan=3, label_font=dim.label_font(14), tooltip="Mostra/Nascondi inset", colorbg="lightgreen")
        row += 1; col = 0
        ui.add_label(position_frame, "Position:", row=row, col=col, colspan=3, colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_entry(position_frame, "x:", self.inset_opt['position']['left'], entry_width=4, row=row, col=col, tooltip="Top", colorbg=color)
        _, col = ui.add_label_entry(position_frame, "y:", self.inset_opt['position']['bottom'], entry_width=4, row=row, col=col, tooltip="Top", colorbg=color)
        row += 1; col = 0
        ui.add_label(position_frame, "Dimension:", row=row, col=col, colspan=3, colorbg=color)
        row += 1; col = 0
        _, col = ui.add_label_entry(position_frame, "⟷", self.inset_opt['position']['width'], entry_width=4, row=row, col=col, tooltip="Top", colorbg=color)
        _, col = ui.add_label_entry(position_frame, "↕", self.inset_opt['position']['height'], entry_width=4, row=row, col=col, tooltip="Top", colorbg=color)

        color = "lightblue"
        body_frame = tk.Frame(self.frame , bg =color, borderwidth=1, relief=tk.SUNKEN)
        body_frame.grid(row=0, column=3)
        row = 0; col = 0
        _, col = ui.add_color(body_frame, self.inset_opt["facecolor"], row=row, col=col, tooltip="Colore di sfondo dell'area del grafico")
        _, col = ui.add_scale(body_frame, self.inset_opt['alpha_face'], from_=0, to=1, resolution=0.05, row=row, col=col, tooltip="Opacità dello sfondo del grafico", colorbg=color)
        
        spine_frame = tk.Frame(body_frame, bg="lightblue", borderwidth=1, relief=tk.SUNKEN)
        spine_frame.grid(row=1, column=0,columnspan=2)
        _, _ = ui.add_label(spine_frame, "┌────", row=0, col=0, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "T", self.inset_opt["spines"]["top"], row=0, col=1, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo superiore", colorbg=color)
        _, _ = ui.add_label(spine_frame, "────┐", row=0, col=2, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "L", self.inset_opt["spines"]["left"], row=1, col=0, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo sinistro", colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "R", self.inset_opt["spines"]["right"], row=1, col=2, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo destro", colorbg=color)
        _, _ = ui.add_label(spine_frame, "└────", row=2, col=0, label_font=dim.label_font(12), colorbg=color)
        _, _ = ui.add_checkbutton(spine_frame, "B", self.inset_opt["spines"]["bottom"], row=2, col=1, label_font=dim.label_font(12), tooltip="Mostra/Nascondi bordo inferiore", colorbg=color)
        _, _ = ui.add_label(spine_frame, "────┘", row=2, col=2, label_font=dim.label_font(12), colorbg=color)
        
        color = "lightgreen"
        grid_frame = tk.Frame(self.frame,borderwidth=1, bg=color, relief=tk.SUNKEN)
        grid_frame.grid(row=0,column=4)
        row = 0; col = 0
        _, col = ui.add_label(grid_frame, "Grid", row=row, col=col, colorbg=color)
        _, col = ui.add_optionmenu(grid_frame, self.inset_opt["grid"]["axis"], AXIS, row=row, col=col, tooltip="Axis", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_optionmenu(grid_frame, self.inset_opt['grid']['style'], LINE, row=row, col=col, tooltip="Grid style", colorbg=color)
        _, col = ui.add_scale(grid_frame, self.inset_opt["grid"]['lw'], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Grid line width", colorbg=color)
        row += 1; col = 0
        _, col = ui.add_color(grid_frame, self.inset_opt["grid"]["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(grid_frame, self.inset_opt["grid"]["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", lenght=80, colorbg=color)

        color ="lightblue"
        sci_frame = tk.Frame(self.frame,borderwidth=1, bg=color, relief=tk.SUNKEN)
        sci_frame.grid(row=0,column=5)
        _, col = ui.add_label(sci_frame, "Scientific notation:", row=0, col=0, colspan=3, tooltip="Scegli tra formato decimale standard o scientifico", colorbg=color)
        _, col = ui.add_optionmenu(sci_frame, self.inset_opt['sci']['style'], ['plain', 'sci'], row=1, col=0, colspan=3, tooltip="Stile:\n⦿ Plain: standard (es. 1000)\n⦿ Sci: scientifico (es. 1e3)", colorbg=color)
        _, col = ui.add_optionmenu(sci_frame, self.inset_opt['sci']['axis'], AXIS, row=2, col=0, colspan=3, tooltip="Asse su cui applicare la notazione", colorbg=color)
        _, col = ui.add_entry(sci_frame, self.inset_opt['sci']['min_scilimits'], entry_width=5, row=3, col=0, tooltip="Limite inferiore per notazione scientifica\n(Es: n → attiva per valori < 10^n)")
        _, col = ui.add_label_entry(sci_frame, "-", self.inset_opt['sci']['max_scilimits'], entry_width=5, row=3, col=1, tooltip="Limite superiore per notazione scientifica\n(Es: m → attiva per valori ≥ 10^m)", colorbg=color)
        
        
        
    def remove_inset(self,inset_id, inset_options, all_inset_id):
        self.inset_opt = None
        if inset_options.get("inset_id") == inset_id:
            inset_options = None
        if inset_id in all_inset_id:
            all_inset_id.remove(inset_id)
            if all_inset_id == ["inset_0"]:
                self.main_page.remove_inset_frame()
        if hasattr(self, "frame") and self.frame:
            self.frame.destroy()
            self.frame = None
        if hasattr(self, "root") and self.root:
            try:
                self.root.destroy()
            except Exception as e:
                print(f"Errore distruggendo il root: {e}")
            self.root = None
        if hasattr(self.root, "update_idletasks"):
            self.root.update_idletasks()

class RegressionApp:
    def __init__(self, root, data_options, file_path):
        frame = root
        self.data_options = data_options
        self.file_path = file_path
                
        # Entry per grado polinomiale (inizialmente nascosta)
        self.pol_degree = tk.IntVar(value=3)
        
        row = 0; col = 0
        # Menù a tendina con i modelli
        self.reg_type = self.data_options["fit"]["type"]  # Mantieni come tk.StringVar
        _, col = ui.add_label(frame, "Fit", row=row, col=col, label_font=("Arial", "12", "bold"), colorbg="lightgreen")
        _, col = ui.add_optionmenu(frame, self.reg_type, REGRESSION_FUNCTIONS, row=row, col=col, tooltip="Funzione di regressione")
        self.degree, col = ui.add_spinbox(frame, self.pol_degree, from_=3, to=20, increment=1, row=row, col=col, tooltip="Degree")
        self.degree.grid_forget()
        _, col = ui.add_label_entry(frame, "Label:", self.data_options["fit"]["label"], entry_width=60, row=row, col=col, columnspan=4)
        row = 1; col = 1
        _, col = ui.add_color(frame, self.data_options["fit"]["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, self.data_options["fit"]["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency")
        _, col = ui.add_optionmenu(frame, self.data_options["fit"]["line"], LINE, row=row, col=col, tooltip="Line")
        _, col = ui.add_scale(frame, self.data_options["fit"]["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line width")
        
        # Funzione che mostra/nasconde entry polinomiale
        def toggle_pol_entry(*args):
            if self.reg_type.get() == "Polynomial":
                self.degree.grid(row=0, column=2)
            else:
                self.degree.grid_forget()
        if hasattr(self.reg_type, "trace_add"):
            self.reg_type.trace_add("write", toggle_pol_entry)
        else:
            self.reg_type.trace("w", lambda *args: toggle_pol_entry())

        # Bottone esecuzione fit
        _, col = ui.add_button(frame, text="Calcola Fit", command=self.run_regression, row=row, col=col)
        show_frame = tk.Frame(frame)
        show_frame.grid(row=row, column=col)
        #_, col = ui.add_optionmenu(frame, self.data_options["plot"]["fit"]["plot_reg"], YN, row=row, col=col, tooltip="Show fit")
        toggle = ToggleSwitch(show_frame, self.data_options["fit"]["plot_reg"],["No","Yes"], tooltip_text="Show Fit")
        toggle.pack() 

        # Label per i risultati
        self.reg_result_label = tk.Label(frame, text="", foreground="blue", justify="left")
        self.reg_result_label.grid(row=0, column=8, columnspan=2, rowspan=2, sticky="w")

    def run_regression(self):
        try:
            reg_type = self.reg_type.get()
            
            common = self.data_options["common"]

            x_col = common["x"].get()
            x_err = common["x_err"].get()
            x2 = common["x2"].get()
            xmin = common["x_min"].get()
            xmax = common["x_max"].get()

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

            if self.data_options['plot_select'].get() == 'plot':
                plot_opt = self.data_options['plot']
                y = plot_opt["y"].get()
                y_err = plot_opt["y_err"].get()
                y2 = plot_opt["y2"].get()
                ymin = plot_opt["y_min"].get()
                ymax = plot_opt["y_max"].get()

                x, y, _, yerr = loader.read(
                    file_path=self.file_path, 
                    x=x_col, y=y, xerr=x_err, yerr=y_err,
                    x2=x2, y2=y2,
                    x_min=xmin,x_max=xmax,y_min=ymin,y_max=ymax,
                    filters1={"cat": col_filter1,"val": filter1,"compare": col_compare_filter1},
                    filters2={"cat": col_filter2,"val": filter2,"compare": col_compare_filter2},
                    filters3={"cat": col_filter3,"val": filter3,"compare": col_compare_filter3},
                    filters4={"cat": col_filter4,"val": filter4,"compare": col_compare_filter4}, 
                    x_fun = common['x_function'].get(), x_par = common['x_parameters'].get(),
                    y_fun = common['y_function'].get(), y_par = common['y_parameters'].get(),
                )
    
            elif self.data_options['plot_select'].get() == 'hist':
                x, _, _, _ = loader.read(
                    file_path=self.file_path, 
                    x=x_col, y=None, xerr=None, yerr=None,
                    x2=x2, y2=None,
                    x_min=xmin,x_max=xmax,y_min=None,y_max=None,
                    filters1={"cat": col_filter1,"val": filter1,"compare": col_compare_filter1},
                    filters2={"cat": col_filter2,"val": filter2,"compare": col_compare_filter2},
                    filters3={"cat": col_filter3,"val": filter3,"compare": col_compare_filter3},
                    filters4={"cat": col_filter4,"val": filter4,"compare": col_compare_filter4}, 
                    x_fun = common['x_function'].get(), x_par = common['x_parameters'].get(),
                    y_fun = None, y_par = None,
                )

                bins_val = int(self.data_options["hist"]["bins"].get())
                density_str = self.data_options["hist"]["density"].get()
                is_density = True if density_str == "True" else False

                x_min_str = self.data_options["common"]["x_min"].get()
                x_max_str = self.data_options["common"]["x_max"].get()
                hist_range = None
                if x_min_str and x_max_str:
                    try:
                        hist_range = (float(x_min_str), float(x_max_str))
                    except ValueError:
                        pass
                y, bin_edges = np.histogram(x, bins=bins_val, range=hist_range, density=is_density)
                x = (bin_edges[:-1] + bin_edges[1:]) / 2
                sigma_fit_input = np.sqrt(y) if not is_density else None
                if sigma_fit_input is not None:
                    sigma_fit_input = np.where(sigma_fit_input == 0, 1, sigma_fit_input)
                yerr = sigma_fit_input
            #print("\n\nreg_ax:",self.x, self.x_err, self.y, self.y_err)
            
            
            
            
            if reg_type == "Linear":
                popt, _ = curve_fit(Functions.linear, x, y, sigma=yerr, absolute_sigma=True)
                y_pred = Functions.linear(x, *popt)

            elif reg_type == "Quadratic":
                popt, _ = curve_fit(Functions.quadratic, x, y, sigma=yerr, absolute_sigma=True)
                y_pred = Functions.quadratic(x, *popt)

            elif reg_type == "Polynomial":
                try:
                    deg = int(self.pol_degree.get())
                    if deg < 1:
                        raise ValueError("The degree must be a positive integer.")
                except ValueError:
                    self.reg_result_label.config(text="Error: polynomial degree is not valid", foreground="red")
                    return
                
                # Gestione pesi per polyfit (w = 1/sigma)
                weights = 1/yerr if yerr is not None else None
                coeffs = np.polyfit(x, y, deg, w=weights)
                popt = coeffs
                y_pred = np.poly1d(coeffs)(x)

            elif reg_type == "Logarithmic":
                mask = x > 0
                popt, _ = curve_fit(Functions.logarithmic, x[mask], y[mask],
                                    sigma=yerr[mask] if yerr is not None else None, absolute_sigma=True)
                x, y = x[mask], y[mask]
                if yerr is not None: yerr = yerr[mask] # Allineo yerr alla mask
                y_pred = Functions.logarithmic(x, *popt)

            elif reg_type == "Exponential":
                popt, _ = curve_fit(Functions.exponential, x, y,
                                    sigma=yerr, absolute_sigma=True, p0=(1, 0.1))
                y_pred = Functions.exponential(x, *popt)

            elif reg_type == "Power law":
                mask = x > 0
                popt, _ = curve_fit(Functions.powerlaw, x[mask], y[mask],
                                    sigma=yerr[mask] if yerr is not None else None, absolute_sigma=True, p0=(1, 1))
                x, y = x[mask], y[mask]
                if yerr is not None: yerr = yerr[mask]
                y_pred = Functions.powerlaw(x, *popt)

            elif reg_type == "Sigmoid":
                p0 = [max(y), np.median(x), 1]
                popt, _ = curve_fit(Functions.sigmoid, x, y,
                                    sigma=yerr, absolute_sigma=True, p0=p0, maxfev=10000)
                y_pred = Functions.sigmoid(x, *popt)

            # --- NUOVE DISTRIBUZIONI STATISTICHE ---

            elif reg_type in ["Gaussian", "Lorentzian", "Skewed Gaussian", "Voigt"]:
                # Calcolo stime iniziali robuste (Media e Sigma pesati)
                # Utile per istogrammi dove y sono conteggi/frequenze
                total_y = np.sum(y)
                if total_y == 0: total_y = 1 # Evita divisione per zero su dati vuoti
                
                mean_guess = np.sum(x * y) / total_y
                sigma_guess = np.sqrt(np.abs(np.sum(y * (x - mean_guess)**2) / total_y))
                if sigma_guess == 0: sigma_guess = 1.0 # Fallback
                amp_guess = np.max(y)

                if reg_type == "Gaussian":
                    p0 = [amp_guess, mean_guess, sigma_guess]
                    popt, _ = curve_fit(Functions.gaussian, x, y, p0=p0, sigma=yerr, absolute_sigma=True, maxfev=10000)
                    y_pred = Functions.gaussian(x, *popt)

                elif reg_type == "Lorentzian":
                    # Gamma per Lorentziana è simile a sigma
                    p0 = [amp_guess, mean_guess, sigma_guess]
                    popt, _ = curve_fit(Functions.lorentzian, x, y, p0=p0, sigma=yerr, absolute_sigma=True, maxfev=10000)
                    y_pred = Functions.lorentzian(x, *popt)

                elif reg_type == "Skewed Gaussian":
                    # Alpha (skew) inizia a 0 (normale)
                    p0 = [amp_guess, mean_guess, sigma_guess, 0]
                    popt, _ = curve_fit(Functions.skewed_gaussian, x, y, p0=p0, sigma=yerr, absolute_sigma=True, maxfev=10000)
                    y_pred = Functions.skewed_gaussian(x, *popt)
                
                elif reg_type == "Voigt":
                    # Voigt ha sigma (Gauss) e gamma (Lorentz). Dividiamo la larghezza stimata.
                    p0 = [amp_guess, mean_guess, sigma_guess/2, sigma_guess/2]
                    popt, _ = curve_fit(Functions.voigt, x, y, p0=p0, sigma=yerr, absolute_sigma=True, maxfev=10000)
                    y_pred = Functions.voigt(x, *popt)

            elif reg_type == "Lognormal":
                mask = x > 0
                # Stima parametri per lognormale
                # s (shape) approx 1, scale (mediana) approx picco
                p0 = [np.max(y), 1.0, np.mean(x)] 
                
                popt, _ = curve_fit(Functions.lognormal, x[mask], y[mask], p0=p0,
                                    sigma=yerr[mask] if yerr is not None else None, absolute_sigma=True, maxfev=10000)
                
                x, y = x[mask], y[mask]
                if yerr is not None: yerr = yerr[mask]
                y_pred = Functions.lognormal(x, *popt)

            elif reg_type == "Exponential PDF":
                # Stima lambda come 1/media
                mean_val = np.abs(np.mean(x)) if np.mean(x) != 0 else 1
                p0 = [np.max(y), 1.0 / mean_val]
                popt, _ = curve_fit(Functions.exponential_pdf, x, y, p0=p0, sigma=yerr, absolute_sigma=True, maxfev=10000)
                y_pred = Functions.exponential_pdf(x, *popt)


            # Calcolo R²
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            if ss_tot == 0:
                r2 = 1.0 if ss_res == 0 else 0.0
            else:
                r2 = 1 - (ss_res / ss_tot)

            # Mostra risultati sul frame
            params_str = "\n".join([f"p{i} = {v:.4g}" for i, v in enumerate(popt)])
            self.reg_result_label.config(
                text=f"{reg_type} fit:\n{params_str}\nR² = {r2:.4f}",
                foreground="blue"
            )
            self.data_options["fit"]["params"] = popt.tolist()  # Salva i parametri del fit nelle opzioni
            self.data_options["fit"]["type"].set(reg_type)  # Aggiorna il tipo di regressione nelle opzioni

        except Exception as e:
            import traceback
            traceback.print_exc()  # Stampa il traceback completo per il debug
            self.reg_result_label.config(text=f"Errore: {e}", foreground="red")
            