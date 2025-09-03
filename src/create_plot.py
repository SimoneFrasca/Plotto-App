import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import font, messagebox, filedialog
from ui_elements import calcola
from ui_elements import convert_file_to_csv, Functions
from matplotlib.colors import to_rgba
import os
import tkinter as tk
import json
import subprocess
import sys

grid_styles = {
    'solid': '-',
    'dotted': ':',
    'dashed': '--',
    'dashdot': '-.'
}

class CreatePlot:
    def __init__(self, root, general_opt, default_opt, data_opt, inset_options, function_options, data_id, inset_id, function_id, save, show):
        self.root = root
        self.data_opt = data_opt
        self.inset_options = inset_options
        self.function_options = function_options
        self.data_id = data_id
        self.inset_id = inset_id
        self.function_id = function_id
        self.extreme = {'min': 0, 'max': 1}
        self.save = save
        self.show = show

        # Default options
        self.general_opt = general_opt
        self.font_opt = general_opt['font']
        self.structure_opt = general_opt['structure']
        self.legend_opt = general_opt['legend']
        self.default_opt = default_opt

        self.canvas = None
        self.fig = None
        self.create_figure()

    def create_figure(self):
        # --- Rimuovi canvas e chiudi figura precedente ---
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.fig:
            plt.close(self.fig)  # Chiudi esplicitamente la figura precedente

        print("-------------------------------------------------------------------------------------------------\nSetting:")
        # Crea un dizionario base con i parametri comuni
        rc_params = {
            "xtick.labelsize": float(self.font_opt["xaxis_size"].get()),
            "ytick.labelsize": float(self.font_opt["yaxis_size"].get()),
            "text.color": self.font_opt["color"].get(),
            "axes.labelcolor": self.font_opt["color"].get(),
            "xtick.color": self.font_opt["color"].get(),
            "ytick.color": self.font_opt["color"].get(),
            "axes.titlecolor": self.font_opt["color"].get()
        }

        # Aggiungi o modifica i parametri in base al valore di tex
        rc_params["text.usetex"] = self.font_opt["tex"].get() == "Yes"
        if rc_params["text.usetex"]:
            rc_params["font.family"] = self.font_opt["main_font"].get()
        # Aggiorna plt.rcParams con il dizionario
        plt.rcParams.update(rc_params)
        
        # --- Crea nuova figura ---
        self.fig, main_ax = plt.subplots(
            figsize=(float(self.structure_opt["x_dim"].get()), float(self.structure_opt["y_dim"].get()))
        )
        print("Figure size:", self.structure_opt["x_dim"].get(), "x", self.structure_opt["y_dim"].get())

        print("Title:", self.structure_opt['title'].get())
        print("X Label:", self.structure_opt['x_label'].get())
        print("Y Label:", self.structure_opt['y_label'].get())
        main_ax.set_title(self.structure_opt['title'].get(), fontsize=float(self.font_opt["title_size"].get()))
        main_ax.set_xlabel(self.structure_opt['x_label'].get(), fontsize=float(self.font_opt["xlabel_size"].get()))
        main_ax.set_ylabel(self.structure_opt['y_label'].get(), fontsize=float(self.font_opt["ylabel_size"].get()))
        
        main_ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        main_ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        main_ax.ticklabel_format(style=self.structure_opt['sci']['style'].get(), axis=self.structure_opt['sci']['axis'].get()
                                 , scilimits=(int(self.structure_opt['sci']['min_scilimits'].get()), int(self.structure_opt['sci']['max_scilimits'].get())))

        main_ax.xaxis.get_offset_text().set_fontsize(float(self.font_opt["xaxis_size"].get()))
        main_ax.yaxis.get_offset_text().set_fontsize(float(self.font_opt["yaxis_size"].get()))

        print("Sci options:", self.structure_opt['sci']['style'].get(), self.structure_opt['sci']['axis'].get(),
              self.structure_opt['sci']['min_scilimits'].get(), self.structure_opt['sci']['max_scilimits'].get())

        grid_option = self.structure_opt["grid"]["style"].get() 
        if grid_option == 'None':
            plt.grid(False)
            print("Grid Options: None")
        else:
            style = self.structure_opt["grid"]['style'].get()
            lw = float(self.structure_opt["grid"]['lw'].get())
            color = self.structure_opt["grid"]['color'].get()
            alpha = float(self.structure_opt["grid"]['alpha'].get())
            axis = self.structure_opt["grid"]['axis'].get()
            plt.grid(True, linestyle=style, linewidth=lw, color=color, alpha=alpha, axis=axis)
            print("Grid Options:", style, "line width:", lw, "color:", color, "alpha:", alpha, "axis:", axis)

        log = self.structure_opt["log"].get()
        if log == 'SemiLog x': main_ax.set_xscale('log')
        elif log == 'SemiLog y': main_ax.set_yscale('log')
        elif log == 'Log Log':
            main_ax.set_xscale('log')
            main_ax.set_yscale('log')

        print("Log:", self.structure_opt["log"].get())
        print("Font:", self.font_opt['main_font'].get(), "Tex:", self.font_opt['tex'].get(),
              "title:", self.font_opt['title_size'].get(), "xlabel:", self.font_opt['xlabel_size'].get(),
              "ylabel:", self.font_opt['ylabel_size'].get(), "xaxis:", self.font_opt['xaxis_size'].get(),
              "yaxis:", self.font_opt['yaxis_size'].get(), "color:", self.font_opt['color'].get())

        # --- Gestione inset ---
        for inset_label in self.inset_id:
            ax = main_ax if inset_label == "inset_0" else self.create_inset(main_ax, inset_label)
            self.plot_data_for_inset(ax, inset_label)
            self.plot_functions_for_inset(ax, inset_label)

        # --- Ottimizza layout ---
        self.fig.tight_layout()  # <- Qui

        if self.legend_opt['legend'].get() == "Yes":
            legend_args = {
                'loc': self.legend_opt['legend_position'].get(),
                'fontsize': self.safe_convert(self.legend_opt['legend_size'].get(), int, 10),
                'title': self.legend_opt['legend_title'].get(),
                'frameon': self.legend_opt['legend_frame'].get() == "Yes",
                'framealpha': self.safe_convert(self.legend_opt['legend_alpha'].get(), float, 1.0),
                'shadow': self.legend_opt['legend_shadow'].get() == "Yes",
                'borderpad': self.safe_convert(self.legend_opt['legend_borderpad'].get(), float, 0.4),
                'labelspacing': self.safe_convert(self.legend_opt['legend_labelspacing'].get(), float, 0.5),
                'handlelength': self.safe_convert(self.legend_opt['legend_handlelength'].get(), float, 2.0),
                'handleheight': self.safe_convert(self.legend_opt['legend_handleheight'].get(), float, 0.7),
                'handletextpad': self.safe_convert(self.legend_opt['legend_handletextpad'].get(), float, 0.8),
                'borderaxespad': self.safe_convert(self.legend_opt['legend_borderaxespad'].get(), float, 0.5),
                'ncol': self.safe_convert(self.legend_opt['legend_ncol'].get(), int, 1),
                'markerscale': self.safe_convert(self.legend_opt['legend_markerscale'].get(), float, 1.0)
            }

            #--- Legend --------------
            plt.legend(**legend_args)
            print("Legend Options:", legend_args)
        else:
            print("Legend: No")

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
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(self.fig) 

        print("-------------------------------------------------------------------------------------------------")

    def show_saved_file(self):
        # --- Apri automaticamente il file salvato ---
        print("ciao")
        if sys.platform.startswith("win"):
            os.startfile(self.save_path)  # Windows
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", self.save_path])  # macOS
        else:
            subprocess.run(["xdg-open", self.save_path])  # Linux

    def save_config_and_data(self, filename):
        def serialize(obj):
            # Caso tkinter Variable
            if hasattr(obj, "get") and callable(obj.get) and not isinstance(obj, dict):
                try:
                    return obj.get()
                except TypeError:
                    # Se è un dict.get travestito, ignora
                    pass
            if isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(i) for i in obj]
            else:
                return obj

        serializable_general_opt = serialize(self.general_opt)
        serializable_default_opt = serialize(self.default_opt)
        serializable_data_opt = serialize(self.data_opt)
        serializable_inset_options = serialize(self.inset_options)
        serializable_function_options = serialize(self.function_options)

        serializable_data_id = list(self.data_id) if hasattr(self, "data_id") else []
        serializable_inset_id = list(self.inset_id) if hasattr(self, "inset_id") else []
        serializable_function_id = list(self.function_id) if hasattr(self, "function_id") else []

        with open(filename, "w") as f:
            json.dump({
                "general_opt": serializable_general_opt,
                "default_opt": serializable_default_opt,
                "data_opt": serializable_data_opt,
                "inset_options": serializable_inset_options,
                "function_options": serializable_function_options,
                "data_id": serializable_data_id,
                "inset_id": serializable_inset_id,
                "function_id": serializable_function_id
            }, f, indent=4)


    def safe_convert(self, value, target_type, default=None):
        try:
            return target_type(value)
        except (ValueError, TypeError):
            return default

    # ----- Configura assi principali/inset -----
    def configure_axes(self, ax, opts):
        common = opts['common']
        grid = opts['grid']
        legend = opts['legend']
        font = opts['font']
        sci = opts['sci']

        ax.set_title(common["title"].get())
        ax.set_xlabel(common["x_label"].get())
        ax.set_ylabel(common["y_label"].get()) 
        
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style=sci['style'].get(), axis=sci['axis'].get()
                                 , scilimits=(int(sci['min_scilimits'].get()), int(sci['max_scilimits'].get())))

        log = opts['common']["log"].get()
        if log == 'SemiLog x': ax.set_xscale('log')
        elif log == 'SemiLog y': ax.set_yscale('log')
        elif log == 'Log Log':
            ax.set_xscale('log')
            ax.set_yscale('log')

        if grid['style'].get() != "None":
            ax.grid(True, linestyle=grid['style'].get(), 
                    linewidth=grid['lw'].get(),
                    color=grid['color'].get(),
                    alpha=float(grid['alpha'].get()),
                    axis=grid['axis'].get())

        legend = opts['legend']
        if legend['legend'].get() == "Yes":
            ax.legend(loc=legend['legend_position'].get(),
                      fontsize=int(legend['legend_size'].get()),
                      frameon=self.legend_opt['legend_frame'].get() == "Yes",
                      shadow=self.legend_opt['legend_shadow'].get() == "Yes",
                      borderpad=float(self.legend_opt['legend_borderpad'].get()),
                      labelspacing=float(self.legend_opt['legend_labelspacing'].get()),
                      handlelength=float(self.legend_opt['legend_handlelength'].get()),
                      handleheight=float(self.legend_opt['legend_handleheight'].get()),
                      handletextpad=float(self.legend_opt['legend_handletextpad'].get()),
                      borderaxespad=float(self.legend_opt['legend_borderaxespad'].get()),
                      ncol=int(self.legend_opt['legend_ncol'].get()),
                      markerscale=float(self.legend_opt['legend_markerscale'].get()))

        font = opts['font']


        # Titolo
        ax.title.set_fontsize(int(font["title_size"].get()))
        # Etichette degli assi (stesso valore per X e Y)
        ax.set_xlabel(ax.get_xlabel(), fontsize=int(font["xlabel_size"].get()))
        ax.set_ylabel(ax.get_ylabel(), fontsize=int(font["ylabel_size"].get()))
        # Tick labels (serve aggiungere xtick_size e ytick_size al dizionario)
        ax.tick_params(axis='x', labelsize=int(font["xaxis_size"].get()))
        ax.tick_params(axis='y', labelsize=int(font["yaxis_size"].get()))
        # Colore (opzionale, se vuoi applicarlo anche qui)
        ax.xaxis.label.set_color(font["color"].get())
        ax.yaxis.label.set_color(font["color"].get())
        ax.title.set_color(font["color"].get())


    def create_inset(self, main_ax, inset_label):
        opts = self.inset_options[inset_label]
        ax = main_ax.inset_axes([
            float(opts['position']["left"].get()),
            float(opts['position']["bottom"].get()),
            float(opts['position']["width"].get()),
            float(opts['position']["height"].get())
        ])
        self.configure_axes(ax, opts)
        return ax

    # ----- Plot dei dati -----
    def plot_data_for_inset(self, ax, inset_label):
        ids = [d for d in self.data_id if inset_label in d]
        for data_id in ids:
            options = self.data_opt[data_id]
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
                

    def plot_functions_for_inset(self, ax, inset_label):
        ids = [f for f in self.function_id if inset_label in f]
        for function_id in ids:
            self.plot_function(self.function_options[function_id], ax)

    # ----- Funzioni di utilità -----
    def safe_float(self, value):
        return float(value) if value else None

    def update_extreme(self, datax):
        self.extreme['min'] = min(self.extreme['min'], min(datax))
        self.extreme['max'] = max(self.extreme['max'], max(datax))

    # ----- Plot semplice -----
    def plot(self, options, ax):
        common = options['common']
        plot_opt = options['plot']
        error_opt = options['plot']['errorbar']
        def_plot_opt = self.default_opt['plot']
        def_errorbar_opt = self.default_opt['plot']['errorbar']
        x_col, y_col = common['x'].get(), plot_opt['y'].get()
        
        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        x_min = float(common["x_min"].get()) if common["x_min"].get() != "" else None
        x_max = float(common["x_max"].get()) if common["x_max"].get() != "" else None
        y_min = float(plot_opt["y_min"].get()) if plot_opt["y_min"].get() != "" else None
        y_max = float(plot_opt["y_max"].get()) if plot_opt["y_max"].get() != "" else None

        datax, datay, xerr, yerr = self.read(
            options['file path'], 
            x_col, y_col, 
            common['x_err'].get(), plot_opt['y_err'].get(),x_min,x_max,y_min,y_max
        )
        self.update_extreme(datax)

        if common['function'].get() != "":
            datay = calcola(datay, common['function'].get(), common['parameters'].get())

        # Parametri comuni per plot/errorbar
        plot_args = {
            'color': self.structure_opt['def_color'].get() if self.structure_opt['def_color'].get() != "None" else common['color'].get(),
            'alpha': float(self.structure_opt['def_color'].get()) if self.structure_opt['def_color'].get() != "None" else float(common['alpha'].get()),
            'linestyle': def_plot_opt['def_line'].get() if def_plot_opt['def_line'].get() != "None" else plot_opt['line'].get(),
            'marker': def_plot_opt['def_marker'].get() if def_plot_opt['def_marker'].get() != "None" else plot_opt['marker'].get(),
            'markersize': float(plot_opt['ms'].get()) if def_plot_opt['def_ms'].get() == "" else float(def_plot_opt['def_ms'].get()),
            'linewidth': float(plot_opt['lw'].get()) if def_plot_opt['def_lw'].get() == "" else float(def_plot_opt['def_lw'].get()),
            'markerfacecolor': plot_opt['mfcolor'].get() if plot_opt["mfc"].get() == "Yes" else common['color'].get(),
            'label': common['label'].get()
        }

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
        
        if plot_opt['fit']['plot_reg'].get() == "Yes":
            x = np.linspace(np.min(datax), np.max(datax), 1000)
            reg_type = plot_opt['fit']['type'].get()
            popt = plot_opt['fit']['params']  # Rimuove .get()

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

            ax.plot(
                x, y,
                linestyle=plot_opt['fit']['line'].get() if plot_opt['fit']['line'].get() != "None" else self.plot_opt['def_line'].get(),
                linewidth=float(plot_opt['fit']['lw'].get()) if plot_opt['fit']['lw'].get() != "" else float(self.plot_opt['def_lw'].get()),
                color=plot_opt['fit']['color'].get() if plot_opt['fit']['color'].get() != "" else self.plot_opt['def_color'].get(),
                alpha=float(plot_opt['fit']['alpha'].get()) if plot_opt['fit']['alpha'].get() != "" else 1.0,
                label=plot_opt['fit']['label'].get() if plot_opt['fit']['label'].get() != "" else None
            )

    # ----- Istogramma -----
    def hist(self, options, ax):
        common = options['common']
        hist_opt = options['hist']
        x = common['x'].get()
        if x == "None":
            messagebox.showerror("Error", "X data not selected.")
            return
        

        x_min = float(common["x_min"].get()) if common["x_min"].get() != "" else None
        x_max = float(common["x_max"].get()) if common["x_max"].get() != "" else None
        
        datax, _, _, _, = self.read(
            options['file path'], x,
            None, None, None, x_min, x_max, None, None
        )

        # preparo i valori
        facecolor = (
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

        # costruisco già i colori RGBA
        face_rgba = to_rgba(facecolor, face_alpha) if facecolor != "None" else "none"
        edge_rgba = to_rgba(edgecolor, contour_alpha)

        # dizionario di argomenti validi per ax.hist
        hist_args = {
            'bins': int(hist_opt['bins'].get()),
            'density': hist_opt['density'].get(),
            'align': hist_opt['align'].get(),
            'orientation': hist_opt['orientation'].get(),
            'cumulative': hist_opt['cumulative'].get(),
            'bottom': float(hist_opt['bottom'].get()),
            'rwidth': float(hist_opt['rwidth'].get()),
            'facecolor': face_rgba,
            'edgecolor': edge_rgba,
            'linewidth': hist_opt['contour_width'].get(),
            'linestyle': hist_opt['contour_line'].get()
        }

        # disegno istogramma
        ax.hist(datax, **hist_args)


    
    # ----- Scatter Plot -----
    def scatter(self, options, ax):
        common = options['common']
        x_col, y_col = common['x'].get(), options['scatter']['y'].get()

        if x_col == "None" or y_col == "None":
            messagebox.showerror("Error", "X or Y data not selected.")
            return

        datax, datay, xerr, yerr = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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

        datax, datay, _, _ = self.read(
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
        Y = calcola(X, expr, parameters)
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
                marker=options['marker'].get() or self.plot_opt['def_marker'].get(),
                markersize=float(options['ms'].get() or self.plot_opt['def_ms'].get() or 6),
                linewidth=float(options['lw'].get() or self.plot_opt['def_lw'].get() or 1)
            )
        #except Exception as e:
        #    print(f"Errore funzione: {e}")

    # ----- Lettura dati -----
    def read(self, file_path, x, y, xerr, yerr,x_min,x_max,y_min,y_max):
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
            
        if x_min is not None and x_max is not None:
            df = df[(df[x] >= x_min) & (df[x] <= x_max)]

        if y_min is not None and y_max is not None:
            df = df[(df[y] >= y_min) & (df[y] <= y_max)]
        
        datax = df[x].values if x else None
        datay = df[y].values if y else None
        xerr_val = df[xerr].values if xerr else None
        yerr_val = df[yerr].values if yerr else None
        return datax, datay, xerr_val, yerr_val


