import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib
matplotlib.use("TkAgg")
from ui_elements import dim, MARKER, LINE, LOG, YN, TF, LEGEND, FONTS, COLOR, HISTTYPE, ORIENTATION, ALIGN, PLOT, REGRESSION_FUNCTIONS, AXIS, Helper, Functions
from ui_elements import convert_file_to_csv, ToggleSwitch
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from ui_elements import calcola
import os
BASE_DIR = os.path.dirname(__file__)

ui = Helper

class DataOptions:
    def __init__(self, root, inset_counter, data_id, file_path, column, data_options, all_data_id, upload=False):
        self.root = root
        self.upload = upload
        
        # Options dictionary
        self.data_options = {
            # Options common to plot and hist
            "data_id": data_id,
            "inset": inset_counter,
            "file path": file_path,            
            "plot_select": tk.StringVar(value="plot"),
            "common": {
                "x": tk.StringVar(value=column[0]),
                "x_min": tk.StringVar(value=""),
                "x_max": tk.StringVar(value=""),
                "x_err": tk.StringVar(value="None"),
                "label": tk.StringVar(),
                "function": tk.StringVar(value=""),
                "parameters": tk.StringVar(value=""),
                "color": tk.StringVar(value=COLOR[0]),
                "alpha": tk.StringVar(value="1")
            },
            # Options specific to plot
            "plot": {
                "y": tk.StringVar(value=column[0]),
                "y_min": tk.StringVar(value=""),
                "y_max": tk.StringVar(value=""),
                "y_err": tk.StringVar(value="None"),
                "marker": tk.StringVar(value=MARKER[0]),
                "ms": tk.StringVar(value="5"),
                "mfc": tk.StringVar(value="No"),
                "mfcolor": tk.StringVar(value=COLOR[0]),
                "line": tk.StringVar(value="None"),
                "lw": tk.StringVar(value="1"),
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
                "errorbar": {
                    "ecolor": tk.StringVar(value=COLOR[0]),
                    "elinewidth": tk.StringVar(value=1.5),
                    "capsize": tk.StringVar(value=3),
                    "capthick": tk.StringVar(value=1.5)
                }
            },
            # Options specific to hist
            "hist": {
                "bins": tk.StringVar(value="10"),
                "align": tk.StringVar(value=ALIGN[0]),
                "density": tk.StringVar(value="False"),
                'orientation': tk.StringVar(value=ORIENTATION[0]), 
                'cumulative': tk.StringVar(value="False"), 
                'bottom': tk.StringVar(value=0), 
                'rwidth': tk.StringVar(value=1),
                'contour_color': tk.StringVar(value='None'),
                'contour_alpha': tk.StringVar(value="1"),
                'contour_width': tk.StringVar(value="1"),
                'contour_line': tk.StringVar(value=LINE[0])
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

        file_label = tk.Label(
            frame,
            text=f"File: {self.data_options['file path'].split('/')[-1]}",
            anchor="w", font=("Arial", 12, "bold"), bg="lightblue"
        )
        # sticky="ew" to allow stretching
        file_label.grid(row=0, column=1, padx=dim.s(5), pady=dim.s(5), sticky="ew")

        ui.add_label_optionmenu(frame, "Mode:", self.data_options["plot_select"], PLOT, row=0, col=2)

        # Arrow button (if you use it)
                # Variable for expansion state
        self.expanded = True  

        # Arrow button (initially "▼")
        self.toggle_button = tk.Button(
            frame, text="▼", width=2, command=lambda: self.toggle_frame(specific_frame)
        )
        self.toggle_button.grid(row=0, column=4, padx=dim.s(5), pady=dim.s(5), sticky="e")


        # ⬅️ GIVE WEIGHT TO COLUMN 1 (the one with the label)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)  # expands to fill
        frame.grid_columnconfigure(2, weight=0)
        frame.grid_columnconfigure(3, weight=0)

        # --- Frame for specific options: takes full width
        specific_frame = tk.Frame(frame, bg="lightblue")
        specific_frame.grid(row=1, column=0, columnspan=5, sticky="ew")
        specific_frame.grid_columnconfigure(0, weight=1)  # to stretch internally, if necessary

    
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
       
    def plot_config(self,specific_frame,column):
        container = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        container.grid(row=0, column=0, sticky="ew")
        canvas = tk.Canvas(container, bg="lightblue", height=dim.s(252), width=dim.s(1000))
        canvas.grid(row=0, column=0, sticky="ew")
        h_scrollbar = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        canvas.configure(xscrollcommand=h_scrollbar.set)
        axis_frame = tk.Frame(canvas, bg="lightblue")
        canvas.create_window((0, 0), window=axis_frame, anchor="nw")
        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        axis_frame.bind("<Configure>", update_scrollregion)
        container.grid_columnconfigure(0, weight=1)
        row, col = 1, 0

        _, col = ui.add_label_entry(axis_frame, "Label:", self.data_options["common"]["label"], entry_width=80, row=row, col=col, columnspan=7,tooltip="Label")
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(axis_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
        _, col = ui.add_label_optionmenu(axis_frame, "X error:", self.data_options["common"]["x_err"], column + ["None"], row=row, col=col)
        _, col = ui.add_label(axis_frame, "X min-max:", row=row, col=col)
        _, col = ui.add_entry(axis_frame, self.data_options["common"]["x_min"], entry_width=8, row=row, col=col)
        _, col = ui.add_label(axis_frame, "-", row=row, col=col)
        _, col = ui.add_entry(axis_frame, self.data_options["common"]["x_max"], entry_width=8, row=row, col=col)
        row += 1; col = 0
        _, col = ui.add_label_optionmenu(axis_frame, "Y:", self.data_options["plot"]["y"], column, row=row, col=col)
        _, col = ui.add_label_optionmenu(axis_frame, "Y error:", self.data_options["plot"]["y_err"], column + ["None"], row=row, col=col)
        _, col = ui.add_label(axis_frame, "Y min-max:", row=row, col=col)
        _, col = ui.add_entry(axis_frame, self.data_options["plot"]["y_min"], entry_width=8, row=row, col=col)
        _, col = ui.add_label(axis_frame, "-", row=row, col=col)
        _, col = ui.add_entry(axis_frame, self.data_options["plot"]["y_max"], entry_width=8, row=row, col=col)
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, "Function:", self.data_options["common"]["function"], entry_width=80, row=row, col=col, columnspan=7,tooltip="Function")
        row += 1; col = 0
        _, col = ui.add_label_entry(axis_frame, "Parameters:", self.data_options["common"]["parameters"], entry_width=80, row=row, col=col, columnspan=7,tooltip="Parameters: inserire\n parametri nel formato\npar1=value1,par2=value2,...")
        
        options_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        options_frame.grid(row=0, column=1, columnspan=1, sticky="ew")
        
        color_frame = tk.Frame(options_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        color_frame.grid(row=0,column=0)
        _, col = ui.add_color(color_frame, self.data_options["common"]["color"], row=0, col=0, tooltip="Color")
        _, col = ui.add_scale(color_frame, self.data_options["common"]["alpha"], from_ = 0, to = 1, resolution = 0.05, row=1, col=0, tooltip="Transparency")
        _, col = ui.add_color(color_frame, self.data_options["plot"]["mfcolor"], row=0, col=1, tooltip="Marker Face Color")
        _, col = ui.add_optionmenu(color_frame, self.data_options["plot"]["mfc"], YN, row=1, col=1, tooltip="Marker Face Color")
        marker_frame = tk.Frame(options_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        marker_frame.grid(row=0,column=1)
        _, col = ui.add_optionmenu(marker_frame, self.data_options["plot"]["marker"], MARKER, row=0, col=0, tooltip="Marker")
        _, col = ui.add_scale(marker_frame, self.data_options["plot"]["ms"], from_=0, to=10, resolution=0.1, row=1, col=0, tooltip="Marker size")
        line_frame = tk.Frame(options_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        line_frame.grid(row=0,column=2)
        _, col = ui.add_optionmenu(line_frame, self.data_options["plot"]["line"], LINE, row=0, col=0, tooltip="Line")
        _, col = ui.add_scale(line_frame, self.data_options["plot"]["lw"], from_=0, to=3, resolution=0.1, row=1, col=0, tooltip="Line width")
        error_frame = tk.Frame(options_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        error_frame.grid(row=2,column=0,columnspan=3)
        row = 0; col = 0
        _, col = ui.add_color(error_frame, self.data_options['plot']["errorbar"]["ecolor"], row=row, col=col, tooltip="Color Errorbar")
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["elinewidth"], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Error line width")
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["capsize"], from_=0, to=10, resolution=0.5, row=row, col=col, tooltip="Cap size")
        _, col = ui.add_scale(error_frame, self.data_options['plot']["errorbar"]["capthick"], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Cap thick")
        
        # Button to create and show regression frame
        def toggle_regression():
            if hasattr(self, "reg_frame") and self.reg_frame.winfo_exists():
                self.reg_frame.destroy()
                toggle_button.config(text="Esegui Fit")
                self.data_options['plot']['fit']['plot_reg'].set("No")
            else:
                self.reg_frame = tk.Frame(specific_frame, bg="lightgreen",borderwidth=1, relief=tk.SUNKEN)
                self.reg_frame.grid(row=2, column=0, columnspan=6, sticky="w")
                RegressionApp(self.reg_frame, self.data_options, self.data_options["file path"])
                toggle_button.config(text="Rimuovi fit")

        # Toggle button
        toggle_button = tk.Button(specific_frame, text="Esegui Fit", command=toggle_regression)
        toggle_button.grid(row=0, column=2, sticky="w", padx=5, pady=5)

    def hist_config(self,specific_frame,column):
        
        main_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        main_frame.grid(row=1,column=0,columnspan=4, sticky="w") 
        row, col = 0, 0
        _, col = ui.add_label_entry(main_frame, "Label:", self.data_options["common"]["label"], entry_width=80, row=row, col=col,tooltip="Label")
        _, col = ui.add_label_optionmenu(main_frame, "X:", self.data_options["common"]["x"], column, row=row, col=col)
        _, col = ui.add_label(main_frame, "X min-max:", row=row, col=col)
        _, col = ui.add_entry(main_frame, self.data_options["common"]["x_min"], entry_width=8, row=row, col=col)
        _, col = ui.add_label(main_frame, "-", row=row, col=col)
        _, col = ui.add_entry(main_frame, self.data_options["common"]["x_max"], entry_width=8, row=row, col=col)
        
        function_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        function_frame.grid(row=2,column=0) 
        row, col = 0, 0
        _, col = ui.add_label_entry(function_frame, "Function:", self.data_options["common"]["function"], entry_width=40, entry_font=("Arial", 13), row=row, col=col, columnspan=7,tooltip="Function")
        row += 1; col = 0
        _, col = ui.add_entry(function_frame, self.data_options["hist"]["bottom"], row=row, col=col, tooltip= "Bottom")
        _, col = ui.add_optionmenu(function_frame, self.data_options["hist"]["density"], TF, row=row, col=col, tooltip="Density")
        _, col = ui.add_optionmenu(function_frame, self.data_options["hist"]["cumulative"], TF, row=row, col=col, tooltip="Cumulative")
        
        option_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        option_frame.grid(row=2,column=1)        
        row = 0; col = 0
        _, col = ui.add_entry(option_frame, self.data_options["hist"]["bins"], row=row, col=col, tooltip="Bins")
        _, col = ui.add_optionmenu(option_frame, self.data_options["hist"]["align"], ALIGN, row=row, col=col, tooltip="Align")
        row += 1; col = 0
        _, col = ui.add_scale(option_frame, self.data_options["hist"]["rwidth"], from_=0, to=1, resolution=0.05, row=row, col=col, tooltip="Bin Width")
        _, col = ui.add_optionmenu(option_frame, self.data_options["hist"]["orientation"], ORIENTATION, row=row, col=col, tooltip="Orientation")
        
        color_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        color_frame.grid(row=2,column=2)
        ui.add_color(color_frame, self.data_options["common"]["color"], row=0, col=0, tooltip="Color")
        ui.add_scale(color_frame, self.data_options["common"]["alpha"], from_=0, to=1, resolution=0.05, row=1, col=0, tooltip="Transparency")
        
        contour_frame = tk.Frame(specific_frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        contour_frame.grid(row=2,column=3)
        ui.add_color(contour_frame, self.data_options["hist"]["contour_color"], row=0, col=0, tooltip="Contour color")
        ui.add_scale(contour_frame, self.data_options["hist"]["contour_alpha"], from_=0, to=1, resolution=0.05, row=1, col=0, tooltip="Contour transparency")
        ui.add_optionmenu(contour_frame, self.data_options["hist"]["contour_line"], LINE, row=0, col=1, tooltip="Contour line")
        ui.add_scale(contour_frame, self.data_options["hist"]["contour_width"], from_=0, to=3, resolution=0.1, row=1, col=1, tooltip="Countour line width")
        
        
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
            "function": tk.StringVar(value=""),
            "parameters": tk.StringVar(value=""),
            "inset": inset_counter,
            "x min": tk.StringVar(value=""),
            "x max": tk.StringVar(value=""),
            "label": tk.StringVar(),
            "marker": tk.StringVar(value="None"),
            "ms": tk.StringVar(value="5"),
            "line": tk.StringVar(value="solid"),
            "lw": tk.StringVar(value="1"),
            "color": tk.StringVar(value=COLOR[0]),
            "alpha": tk.StringVar(value="1"),
        }
    
        self.options(function_options, function_id, all_function_id)
        function_options[function_id] = self.function_options

    def options(self,function_options, function_id, all_function_id):
        # Main frame
        frame = tk.Frame(self.root, relief=tk.SUNKEN, borderwidth=1)
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
        
        func_frame = tk.Frame(frame, relief=tk.SUNKEN, borderwidth=1)
        func_frame.grid(row = 0, column = 1, padx=dim.s(5), pady=dim.s(5))
        _, col = ui.add_label_entry(func_frame, "Function:", self.function_options["function"], entry_width=45, entry_font=("Arial", 13), row=0, col=0, columnspan=5)
        _, col = ui.add_label_entry(func_frame, "Parameters:", self.function_options["parameters"], entry_width=90, row=1, col=0, columnspan=5, tooltip="Parameters: inserire\n parametri nel formato\npar1=value1,par2=value2,...")
        row = 2; col = 0
        _, col = ui.add_label_entry(func_frame, "Label:", self.function_options["label"], entry_width=50, row=row, col=0)
        _, col = ui.add_label(func_frame, "X min-max",row=row, col=col)
        _, col = ui.add_entry(func_frame, self.function_options["x min"], entry_width=8, row=row, col=col)
        _, col = ui.add_label(func_frame, "-",row=row, col=col)
        _, col = ui.add_entry(func_frame, self.function_options["x max"], entry_width=8, row=row, col=col)
        
        opt_frame = tk.Frame(frame, relief=tk.SUNKEN, borderwidth=1)
        opt_frame.grid(row = 0, column = 2, padx=dim.s(5), pady=dim.s(5))
        row = 0; col = 0
        _, col = ui.add_color(opt_frame, self.function_options["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(opt_frame, self.function_options["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency")
        row += 1; col = 0
        _, col = ui.add_optionmenu(opt_frame, self.function_options["line"], LINE, row=row, col=col, tooltip="Line")
        _, col = ui.add_scale(opt_frame, self.function_options["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line Width")
        
        
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
            'common': {
                'x_dim': tk.StringVar(value=8), 
                'y_dim': tk.StringVar(value=6), 
                'title': tk.StringVar(value=None),
                'x_label': tk.StringVar(value=None), 
                'y_label': tk.StringVar(value=None),
                'x_min': tk.StringVar(value=None), 
                'x_max': tk.StringVar(value=None),
                'y_min': tk.StringVar(value=None), 
                'y_max': tk.StringVar(value=None),
                'log': tk.StringVar(value="None"),
            },
            'grid': {
                'style': tk.StringVar(value='None'),
                'lw': tk.StringVar(value=0.5),
                'color': tk.StringVar(value=COLOR[0]),
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
                "xlabel_size": tk.StringVar(value="10"),        # X axis label size
                "ylabel_size": tk.StringVar(value="10"),        # Y axis label size
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
        
        main_frame = tk.Frame(self.frame, bg="lightblue",borderwidth=1, relief=tk.SUNKEN)
        main_frame.grid(row=0,column=1)
        row = 0; col = 0
        _, col = ui.add_label_entry(main_frame, "Title:", self.inset_opt['common']['title'], entry_width= 50, row=row, col=col, columnspan=5)
        row += 1; col = 0
        _, col = ui.add_label(main_frame, "X/Y dim:", row=row, col=col)
        _, col = ui.add_entry(main_frame, self.inset_opt['common']['x_dim'], entry_width=8, row=row, col=col)
        _, col = ui.add_label(main_frame, "-", row=row, col=col)
        _, col = ui.add_entry(main_frame, self.inset_opt['common']['y_dim'], entry_width=8, row=row, col=col)
        _, col = ui.add_label_optionmenu(main_frame, "Log:", self.inset_opt['common']['log'], LOG, row=row, col=col)
        row += 1; col = 0
        _, col = ui.add_label_entry(main_frame, 'X label', self.inset_opt['common']['x_label'], entry_width=20, row=row, col=col, columnspan=3)
        _, col = ui.add_label_entry(main_frame, 'Y label', self.inset_opt['common']['y_label'], entry_width=20, row=row, col=col+2)
        
        
        position_frame = tk.Frame(self.frame,borderwidth=1, relief=tk.SUNKEN)
        position_frame.grid(row=0,column=2)
        row += 1; col = 0
        ui.add_label(position_frame, "Position:", row=0, col=0, colspan=3)
        row += 1; col = 0
        _, col = ui.add_label_entry(position_frame, "x:", self.inset_opt['position']['left'], entry_width=6, row=row, col=col, tooltip="Top")
        _, col = ui.add_label_entry(position_frame, "y:", self.inset_opt['position']['bottom'], entry_width=6, row=row, col=col, tooltip="Top")
        ui.add_label(position_frame, "Dimension:", row=2, col=0, colspan=3)
        row = 1; col = 0
        _, col = ui.add_label_entry(position_frame, "↕", self.inset_opt['position']['height'], entry_width=6, row=row, col=col, tooltip="Top")
        _, col = ui.add_label_entry(position_frame, "⟷", self.inset_opt['position']['width'], entry_width=6, row=row, col=col, tooltip="Top")

        grid_frame = tk.Frame(self.frame,borderwidth=1, relief=tk.SUNKEN)
        grid_frame.grid(row=0,column=3)
        grid_frame1 = tk.Frame(grid_frame)
        grid_frame1.grid(row=0,column=0)
        row = 0; col = 0
        _, col = ui.add_optionmenu(grid_frame1, self.inset_opt['grid']['style'], LINE, row=row, col=col, tooltip="Grid style")
        _, col = ui.add_optionmenu(grid_frame1, self.inset_opt["grid"]["axis"], AXIS, row=row, col=col, tooltip="Axis")
        _, col = ui.add_color(grid_frame1, self.inset_opt["grid"]["color"], row=row, col=col, tooltip="Color")
        grid_frame2 = tk.Frame(grid_frame)
        grid_frame2.grid(row=1,column=0)
        row = 0; col = 0
        _, col = ui.add_scale(grid_frame2, self.inset_opt["grid"]["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency", lenght=80)
        _, col = ui.add_scale(grid_frame2, self.inset_opt["grid"]['lw'], from_=0, to=3, resolution=0.1, row=row, col=col, tooltip="Grid line width", lenght=80)

        sci_frame = tk.Frame(self.frame,borderwidth=1, relief=tk.SUNKEN)
        sci_frame.grid(row=0,column=4)
        row = 0; col = 0
        _, col = ui.add_optionmenu(sci_frame, self.inset_opt['sci']['style'], ['plain', 'sci'], row=row, col=col, tooltip="Sci style")
        row += 1; col = 0
        _, col = ui.add_optionmenu(sci_frame, self.inset_opt["sci"]["axis"], AXIS, row=row, col=col, tooltip="Sci axis")
        row += 1; col = 0
        sci_frame1 = tk.Frame(sci_frame)
        sci_frame1.grid(row=2,column=0)
        row = 0; col = 0        
        _, col = ui.add_entry(sci_frame1, self.inset_opt["sci"]["min_scilimits"], entry_width=5 , row=row, col=col, tooltip="Sci limits")
        _, col = ui.add_label_entry(sci_frame1, "-", self.inset_opt["sci"]["max_scilimits"], entry_width=5 , row=row, col=col, tooltip="Sci limits")

        legend_frame = tk.Frame(self.frame,borderwidth=1, relief=tk.SUNKEN)
        legend_frame.grid(row=0,column=5)
        row = 0; col = 0
        _, col = ui.add_optionmenu(legend_frame, self.inset_opt['legend']['legend'], YN, row=row, col=col, tooltip="Show legend")
        row += 1; col = 0
        _, col = ui.add_entry(legend_frame, self.inset_opt['legend']['legend_size'], entry_width=6, row=row, col=col, tooltip="Size")
        row += 1; col = 0
        _, col = ui.add_optionmenu(legend_frame, self.inset_opt['legend']['legend_position'], LEGEND, row=row, col=col, tooltip="Position")

        font_frame = tk.Frame(self.frame,borderwidth=1, relief=tk.SUNKEN)
        font_frame.grid(row=0,column=6)
        row = 0; col = 0
        _, col = ui.add_label_entry(font_frame, "Title:", self.inset_opt['font']['title_size'], entry_width=6, row=row, col=col, tooltip="Top")
        _,col = ui.add_label(font_frame, "", row=row, col=col)  # Spacer
        _, col = ui.add_color(font_frame, self.inset_opt['font']["color"], row=row, col=col, tooltip="Color")
        row += 1; col = 0
        _, col = ui.add_label_entry(font_frame, "X/Y label:", self.inset_opt['font']['xlabel_size'], entry_width=6, row=row, col=col, tooltip="Top")
        _, col = ui.add_label_entry(font_frame, "-", self.inset_opt['font']['ylabel_size'], entry_width=6, row=row, col=col, tooltip="Top")
        row += 1; col = 0
        _, col = ui.add_label_entry(font_frame, "X/Y axis:", self.inset_opt['font']['xaxis_size'], entry_width=6, row=row, col=col, tooltip="Top")
        _, col = ui.add_label_entry(font_frame, "-", self.inset_opt['font']['yaxis_size'], entry_width=6, row=row, col=col, tooltip="Top")
        
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
        self.reg_type = self.data_options["plot"]["fit"]["type"]  # Mantieni come tk.StringVar
        _, col = ui.add_label(frame, "Fit", row=row, col=col, label_font=("Arial", "12", "bold"))
        _, col = ui.add_optionmenu(frame, self.reg_type, REGRESSION_FUNCTIONS, row=row, col=col, tooltip="Funzione di regressione")
        self.degree, col = ui.add_spinbox(frame, self.pol_degree, from_=3, to=20, increment=1, row=row, col=col, tooltip="Degree")
        self.degree.grid_forget()
        _, col = ui.add_label_entry(frame, "Label:", self.data_options["plot"]["fit"]["label"], entry_width=60, row=row, col=col, columnspan=4)
        row = 1; col = 1
        _, col = ui.add_color(frame, self.data_options["plot"]["fit"]["color"], row=row, col=col, tooltip="Color")
        _, col = ui.add_scale(frame, self.data_options["plot"]["fit"]["alpha"], from_ = 0, to = 1, resolution = 0.05, row=row, col=col, tooltip="Transparency")
        _, col = ui.add_optionmenu(frame, self.data_options["plot"]["fit"]["line"], LINE, row=row, col=col, tooltip="Line")
        _, col = ui.add_scale(frame, self.data_options["plot"]["fit"]["lw"], from_ = 0, to = 3, resolution = 0.1, row=row, col=col, tooltip="Line width")
        
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
        toggle = ToggleSwitch(show_frame, self.data_options["plot"]["fit"]["plot_reg"],["No","Yes"], tooltip_text="Show Fit")
        toggle.pack() 

        # Label per i risultati
        self.reg_result_label = tk.Label(frame, text="", foreground="blue", justify="left")
        self.reg_result_label.grid(row=0, column=8, columnspan=2, rowspan=2, sticky="w")

    def run_regression(self):
        try:
            reg_type = self.reg_type.get()
            
            self.x = self.data_options["common"]["x"].get()
            self.x_err = self.data_options["common"]["x_err"].get()
            self.y = self.data_options["plot"]["y"].get()
            self.y_err = self.data_options["plot"]["y_err"].get()
            
            print("\n\nreg_ax:",self.x, self.x_err, self.y, self.y_err)
            
            x, y, xerr, yerr = self.read(self.file_path, self.x, self.y, self.x_err, self.y_err)

            if reg_type == "Linear":
                popt, _ = curve_fit(Functions.linear, x, y)
                y_pred = Functions.linear(x, *popt)

            elif reg_type == "Quadratic":
                popt, _ = curve_fit(Functions.quadratic, x, y)
                y_pred = Functions.quadratic(x, *popt)

            elif reg_type == "Polynomial":
                try:
                    deg = int(self.pol_degree.get())
                    if deg < 1:
                        raise ValueError("The degree must be a positive integer.")
                except ValueError:
                    self.reg_result_label.config(text="Error: polynomial degree is not valid", foreground="red")
                    return
                
                coeffs = np.polyfit(x, y, deg)
                popt = coeffs
                y_pred = np.poly1d(coeffs)(x)

            elif reg_type == "Logarithmic":
                mask = x > 0
                popt, _ = curve_fit(Functions.logarithmic, x[mask], y[mask])
                x, y = x[mask], y[mask]
                y_pred = Functions.logarithmic(x, *popt)

            elif reg_type == "Exponential":
                popt, _ = curve_fit(Functions.exponential, x, y, p0=(1, 0.1))
                y_pred = Functions.exponential(x, *popt)

            elif reg_type == "Power law":
                mask = x > 0
                popt, _ = curve_fit(Functions.powerlaw, x[mask], y[mask], p0=(1, 1))
                x, y = x[mask], y[mask]
                y_pred = Functions.powerlaw(x, *popt)

            elif reg_type == "Sigmoid":
                p0 = [max(y), np.median(x), 1]
                popt, _ = curve_fit(Functions.sigmoid, x, y, p0=p0, maxfev=10000)
                y_pred = Functions.sigmoid(x, *popt)

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
            self.data_options["plot"]["fit"]["params"] = popt.tolist()  # Salva i parametri del fit nelle opzioni
            self.data_options["plot"]["fit"]["type"].set(reg_type)  # Aggiorna il tipo di regressione nelle opzioni

        except Exception as e:
            import traceback
            traceback.print_exc()  # Stampa il traceback completo per il debug
            self.reg_result_label.config(text=f"Errore: {e}", foreground="red")
            
    def read(self, file_path, x, y, xerr, yerr):
        if file_path.endswith('.txt'):
            file_path = convert_file_to_csv(file_path)
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xml'):
            df = pd.read_xml(file_path)
        else:
            raise ValueError("Formato file non supportato")
        
        df = df.replace(r'^\s*-?nan\s*$', np.nan, regex=True)
        
        # Rimuove le colonne 'None'
        if x == "None": x = None
        if y == "None": y = None
        if xerr == "None": xerr = None
        if yerr == "None": yerr = None
                
        # Dropna solo sulle colonne effettive
        cols_to_check = [c for c in [x, y] if c is not None]
        df = df.dropna(subset=cols_to_check)
        
        # Ordina se possibile
        if x is not None:
            df = df.sort_values(by=x)
        
        # Controlla se le colonne esistono nel DataFrame
        if x and x not in df.columns:
            raise ValueError(f"La colonna '{x}' non esiste nel file.")
        if y and y not in df.columns:
            raise ValueError(f"La colonna '{y}' non esiste nel file.")
        
        datax = df[x].values if x else None
        datay = df[y].values if y else None
        xerr_val = df[xerr].values if xerr else None
        yerr_val = df[yerr].values if yerr else None

        if self.data_options['common']['function'].get() != "":
            datay = calcola(datay, self.data_options['common']['function'].get(), self.data_options['common']['parameters'].get())
        
        if datax is None or datay is None:
            raise ValueError("Le colonne X e Y devono essere specificate.")
        return datax, datay, xerr_val, yerr_val