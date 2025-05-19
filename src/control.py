# Controller.py
from src.model import AntibiogramModel
from src.view import AntibiogramView

import tkinter.messagebox
import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AntibiogramController:
    def __init__(self):
        self.model = AntibiogramModel()
        self.antibiotics = list(self.model.resistance_thresholds.keys())
        self.view = AntibiogramView(self, self.antibiotics)

    def add_data(self, antibiotic, diameter):
        if self.model.add_data(antibiotic, diameter):
            self.update_results()
        else:
            tkinter.messagebox.showerror("Error", "Invalid diameter value.")

    def update_results(self):
        results = self.model.get_results()
        self.view.update_results_text(results)

    def show_statistics(self):
        mean, std_np, std_scipy = self.model.get_statistics()
        if mean is None:
            tkinter.messagebox.showinfo("Statistics", "No data available.")
        else:
            msg = (f"Mean Diameter: {mean:.2f} mm\n"
                   f"Standard Deviation (NumPy): {std_np:.2f} mm\n"
                   f"Standard Deviation (SciPy): {std_scipy:.2f} mm")
            tkinter.messagebox.showinfo("Statistics", msg)

    def show_graph_popup(self):
        popup = ctk.CTkToplevel(self.view)
        popup.title("Graph Popup")
        popup.geometry("600x400")

        figure = Figure(figsize=(5, 4), dpi=100)
        ax = figure.add_subplot(111)
        self.model.create_graph(ax)

        canvas = FigureCanvasTkAgg(figure, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_comparison(self, ab1, ab2):
        t_stat, p_val = self.model.compare_two_antibiotics(ab1, ab2)
        if t_stat is None:
            tkinter.messagebox.showinfo("Comparison", "Not enough data for comparison.")
        else:
            tkinter.messagebox.showinfo("Comparison", f"T-statistic: {t_stat:.2f}\nP-value: {p_val:.4f}")

    def run(self):
        self.view.mainloop()
