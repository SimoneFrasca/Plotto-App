#------------------------------------------------------------------------------------------------------
# 
#   o             o  oooooo  o        ooooo   oooo   o     o  oooooo       oooo   o   o
#    o     o     o   o       o       o       o    o  oo   oo  o           o    o  oo  o
#     o   o o   o    oooo    o       o       o    o  o o o o  oooo        o    o  o o o
#      o o   o o     o       o       o       o    o  o  o  o  o           o    o  o  oo
#       o     o      oooooo  oooooo   ooooo   oooo   o     o  oooooo       oooo   o   o
#
#                                                                           ^
#                                                                           |                   .
#                        oooooo  o       oooooo  ooooo  ooooo  oooooo       |              .
#                        o    o  o       o    o    o      o    o    o       |          . 
#                        oooooo  o       o    o    o      o    o    o       |      . 
#                        o       o       o    o    o      o    o    o       |   .
#                        o       oooooo  oooooo    o      o    oooooo       | .
#                                                                          -|--------------------->
#
#----------------------------------------------------------------------------------------------------
#
# READ ME
#
# Version 3.1 (Date: /2025)
# Next release: Boh
#
# Before you start use this code veify to own this packages:
# 1) pip install Pillow
# 2) pip install matplotlib
# 3) pip install pandas
# 4) pip install numpy
# 5) pip install tkinter
#
# This code is a simple data plotter that allows you to plot multiple data files on the same graph.
# You can choose to plot your data using different marker styles, line styles, and colors for the plot.
# It is possible to customize the dimensions of the plot, the grid, and the axis limits. You can
# also label the axes and the title of the plot and choose to display a legend.
# For the moment only CSV and XML files are allowed. Plot is saved by default as PDF
#
# An overview of the main features of the code:
#   root : Tk
#        The root window of the Tkinter application.
#    config : dict
#        Configuration settings for the plot.
#    files : list
#        List to store file paths of the data files.
#    data : list
#        List to store data from the files.
#    plot_options : dict
#        Dictionary to store plot configurations for each file.
#    marker : list
#        List of marker styles for the plot.
#    color : list
#        List of colors for the plot.
#    line : list
#        List of line styles for the plot.
#    log : list
#        List of logarithmic options for the plot.
#    yn : list
#        List of Yes/No options.
#    legend : list
#        List of legend positions.
#    color_index : int
#        Index to keep track of the current color.
#    Methods:
#    --------
#    update_limits(*args):
#        Updates the axis limits based on the selected columns.
#    submit():
#        Submits the plot configuration and plots the data.
#    main_options():
#        Creates the main options for the plot configuration.
#    axis_options():
#        Creates the axis options for the plot configuration.
#    data_options(file_config_frame, file_path):
#        Creates the data options for a specific file.
#    main_data():
#        Opens a file dialog to select the main data file and updates the UI.
#    add_new_data():
#        Opens a file dialog to select a new data file and updates the UI.
#    create_file_config(file_path):
#        Creates the file configuration for a specific file.
#    plot_data():
#        Plots the data based on the configuration settings.
    

import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from PIL import Image, ImageTk
from main import MainPage
from ui_elements import root, dim
import os
BASE_DIR = os.path.dirname(__file__)

class DataPlotterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Data Plotter")
        self.setup_ui()

    def setup_ui(self):
        # Sfondo
        
        image = Image.open(os.path.join(BASE_DIR, "sfondo.png"))
        image = image.resize((dim.s(700), dim.s(300)))
        self.wallpaper = ImageTk.PhotoImage(image)

        # Pulsante principale con immagine
        self.main_button_frame = tk.Frame(self.root)
        self.main_button_frame.grid(pady=dim.s(10))

        rows = 0
        tk.Button(self.main_button_frame, image=self.wallpaper, command=self.saluto).grid(row=rows, padx=dim.s(5), pady=dim.s(5))
        rows += 1

        self.add_data_button = tk.Button(self.main_button_frame,text="Start a New Plot",command=self.plot,font=LABEL_FONT)
        self.add_data_button.grid(row=rows, pady=dim.s(10))
        rows += 1

        self.upload_data_button = tk.Button(self.main_button_frame,text="Upload Configuration",command=self.upload_configuration,font=LABEL_FONT)
        self.upload_data_button.grid(row=rows, pady=dim.s(10))
        rows += 1

        # Spazio vuoto
        tk.Label(self.main_button_frame, text="", font=LABEL_FONT).grid(row=rows, pady=dim.s(30))
        rows += 1

        # Testo licenza
        tk.Label(self.main_button_frame, text="Open source program, No one owns it", font=LABEL_FONT).grid(row=rows, pady=dim.s(5))
        rows += 1

        # Icona no copyright
        image = Image.open(os.path.join(BASE_DIR, "no_copyright.png"))
        image = image.resize((dim.s(20), dim.s(20)))
        self.no_copy = ImageTk.PhotoImage(image)
        tk.Label(self.main_button_frame, image=self.no_copy).grid(row=rows, pady=dim.s(5))

    def plot(self):
        MainPage(self,self.root)

    def upload_configuration(self):
        MainPage(self,self.root,upload_configuration=True)

    def saluto(self):
        print("Welcome on Plotto =)")

if __name__ == "__main__":
    LABEL_FONT = dim.label_font()
    app = DataPlotterApp(root)
    root.mainloop()
