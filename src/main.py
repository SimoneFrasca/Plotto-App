from fileinput import filename
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
from ui_elements import dim, convert_file_to_csv, ToolTip
from default_options import GeneralOptions, LegendOptions, FontOptions, LatexConvert
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
        self.data_id = []
        self.inset_id = ["inset_0"]
        self.function_id = []
        self.data_options = {}
        self.inset_options = {}
        self.function_options = {}
        self.general_options = {    
            "structure": GeneralOptions().general_opt,
            "font": FontOptions().font_options,
            "legend": LegendOptions().legend
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
        self.inset_counter = 1
        self.data_counter = [0]
        self.function_counter = [0]

        if upload_configuration:
            self.upload()

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
        self.main_frame = tk.Frame(master)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

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

        if upload_configuration:
            print("ciao")
            # Ricostruisci GUI a partire dai dati caricati
            self.add_inset_frame()
            for inset_id in self.inset_id:
                if inset_id != "inset_0":
                    print(inset_id,self.inset_options[inset_id]['inset'])
                    self.add_inset(True,inset_id,self.inset_options[inset_id]['inset'])
            
            for data_id in self.data_id:
                if (self.data_options[data_id]['inset']) == 0:
                    self.add_file(self.scrollable_frame, 0, data_id, self.data_options[data_id]['file path'], True)
                    
            for function_id in self.function_id:
                if (self.function_options[function_id]['inset']) == 0:
                    self.add_function(self.scrollable_function_frame, 0, function_id, True)

            messagebox.showinfo("Upload completed", f"Configuration uploaded from:\n{self.filename}")
            upload_configuration = False

    def menu_bar(self, master, frame):
        master.grid_columnconfigure(0, weight=1)

        tk.Button(frame, text="File", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("file")).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame, text="General Options", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("opzioni_gen")).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(frame, text="Legend", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("opzioni_legend")).grid(row=0, column=2, padx=2, pady=2)
        tk.Button(frame, text="Font", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("opzioni_font")).grid(row=0, column=3, padx=2, pady=2)
        tk.Button(frame, text="Default Plot Options", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("default")).grid(row=0, column=4, padx=2, pady=2)
        tk.Button(frame, text="Add Inset", font=LABEL_FONT,
                  command=lambda: self.add_inset_frame()).grid(row=0, column=5, padx=2, pady=2)
        tk.Button(frame, text="Latex → Numpy converter", font=LABEL_FONT,
                  command=lambda: self.toggle_manager.toggle("latex_convert")).grid(row=0, column=6, padx=2, pady=2)

    def add_inset_frame(self):
        self.data_menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, rowspan=1)
        self.menu_frame_inset.grid()  
        
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
        if not upload:
            file_path = filedialog.askopenfilename(
                title="Seleziona un file",
                filetypes=[("CSV Files", "*.csv"), ("XML Files", "*.xml"), ("Text Files", "*.txt")]
            )
            if not file_path:
                return
            data_id = f"inset_{inset_counter}_data_{int(self.data_counter[inset_counter])}"
            while data_id in self.data_id:  
                self.data_counter[inset_counter] += 1
                data_id = f"inset_{inset_counter}_data_{int(self.data_counter[inset_counter])}"
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
        if not upload:
            function_id = f"inset_{inset_counter}_function_{int(self.function_counter[inset_counter])}"
            while function_id in self.function_id:  
                self.function_counter[inset_counter] += 1
                function_id = f"inset_{inset_counter}_function_{int(self.function_counter[inset_counter])}"
            self.function_id.append(function_id)

        InsertFunction(frame, inset_counter, function_id, self.function_options, self.function_id, upload)
        
    def add_inset(self,upload=False,inset_id=None,inset_index=None):
        frame = tk.Frame(self.scrollable_inset_frame, relief=tk.SUNKEN, borderwidth=2)
        frame.pack(padx=dim.s(5), pady=dim.s(5), fill=tk.X)
        if not upload:
            inset_index = self.inset_counter  # salva valore attuale
            # Aggiorna inset_id e contatore
            inset_id = f"inset_{inset_index}"
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
        
        def to_stringvar(d, parent_key=None):
            if isinstance(d, dict):
                return {k: to_stringvar(v, parent_key=k) for k, v in d.items()}
            elif isinstance(d, list):
                return [to_stringvar(x, parent_key=parent_key) for x in d]
            elif isinstance(d, str):
                # Non wrappare i percorsi file
                if parent_key == "file path":
                    return d
                return tk.StringVar(value=d)
            else:
                return d

        try:
            with open(self.filename, "r") as f:
                saved_data = json.load(f)

            # Ricostruisci gli oggetti con StringVar
            #print(saved_data.get("general_opt"))
            self.general_options   = to_stringvar(saved_data.get("general_opt", {}))
            self.default_options   = to_stringvar(saved_data.get("default_opt", {}))
            self.data_options      = to_stringvar(saved_data.get("data_opt", {}))
            #print(self.data_options['inset_0']['common']['x'].get())
            self.inset_options     = to_stringvar(saved_data.get("inset_options", {}))
            self.function_options  = to_stringvar(saved_data.get("function_options", {}))
            self.data_id           = saved_data.get("data_id", [])
            self.inset_id          = saved_data.get("inset_id", ["inset_0"])
            self.function_id       = saved_data.get("function_id", [])
        
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile caricare la configurazione:\n{e}")
       
    def back_to_main(self):
        # Clear the existing content in the root window
        self.main_frame.destroy()
        self.menu_bar_frame.destroy()
        self.menu_frame.destroy()
        
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
            "opzioni_legend": lambda: LegendOptions().options(self.content_frame, general_options['legend']),
            "opzioni_font": lambda: FontOptions().options(self.content_frame, general_options['font']),
            "default": lambda: main_page.default_buttons(self.content_frame),
            "latex_convert": lambda: LatexConvert().convertion(self.content_frame),

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
        if key in ["file", "opzioni_gen", "opzioni_legend", "opzioni_font", "default", "latex_convert"]:
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
