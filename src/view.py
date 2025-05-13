# View.py
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AntibiogramView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Antibiogram Result Analysis")

        self.antibiotic_label = ttk.Label(self, text="Antibiotic:")
        self.antibiotic_entry = ttk.Entry(self)

        self.diameter_label = ttk.Label(self, text="Inhibition Zone Diameter (mm):")
        self.diameter_entry = ttk.Entry(self)

        self.add_button = ttk.Button(self, text="Add Data", command=self.add_click)

        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_text = tk.Text(self.results_frame, height=10, width=50)
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=self.results_scrollbar.set)

        self.graph_frame = ttk.LabelFrame(self, text="Graph")
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.widget = self.canvas.get_tk_widget()

        self.update_button = ttk.Button(self, text="Update Graph", command=self.update_click)

        self.grid_elements()

    def grid_elements(self):
        self.antibiotic_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.antibiotic_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.diameter_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.diameter_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.results_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.results_text.pack(side="left", fill="both", expand=True)
        self.results_scrollbar.pack(side="right", fill="y")

        self.graph_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.widget.pack(fill="both", expand=True)

        self.update_button.grid(row=5, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def add_click(self):
        antibiotic = self.antibiotic_entry.get()
        diameter = self.diameter_entry.get()
        self.controller.add_data(antibiotic, diameter)
        self.antibiotic_entry.delete(0, tk.END)
        self.diameter_entry.delete(0, tk.END)

    def update_results_text(self, results_df):
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, results_df.to_string())

    def update_graph(self):
        self.controller.update_graph(self.axes)
        self.canvas.draw()

    def update_click(self):
        self.controller.update_results()