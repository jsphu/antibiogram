import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ----------------- MODEL -----------------
class AntibiogramModel:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Antibiotic', 'Inhibition Zone Diameter (mm)'])
        self.resistance_thresholds = {
            'Penicillin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
            'Cefazolin': {'susceptible': 18, 'intermediate': 15, 'resistant': 14},
            'Erythromycin': {'susceptible': 18, 'intermediate': 14, 'resistant': 13},
            'Tetracycline': {'susceptible': 19, 'intermediate': 15, 'resistant': 14},
            'Gentamicin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
        }

    def add_data(self, antibiotic, diameter):
        try:
            diameter = float(diameter)
            self.data = pd.concat(
                [self.data, pd.DataFrame([{'Antibiotic': antibiotic, 'Inhibition Zone Diameter (mm)': diameter}])],
                ignore_index=True
            )
            return True
        except ValueError:
            return False

    def interpret_resistance(self, diameter, antibiotic):
        if antibiotic in self.resistance_thresholds:
            thresholds = self.resistance_thresholds[antibiotic]
            if diameter >= thresholds['susceptible']:
                return "Susceptible"
            elif thresholds['intermediate'] <= diameter < thresholds['susceptible']:
                return "Intermediate"
            else:
                return "Resistant"
        else:
            return "No Threshold Data"

    def get_results(self):
        results = []
        for _, row in self.data.iterrows():
            antibiotic = row['Antibiotic']
            diameter = row['Inhibition Zone Diameter (mm)']
            interpretation = self.interpret_resistance(diameter, antibiotic)
            results.append({'Antibiotic': antibiotic, 'Diameter': diameter, 'Result': interpretation})
        return pd.DataFrame(results)

    def get_graph_data(self):
        return self.data['Antibiotic'].tolist(), self.data['Inhibition Zone Diameter (mm)'].tolist()

    def create_graph(self, ax):
        antibiotics, diameters = self.get_graph_data()
        ax.clear()
        ax.bar(antibiotics, diameters, color='skyblue')
        ax.set_xlabel("Antibiotic")
        ax.set_ylabel("Inhibition Zone Diameter (mm)")
        ax.set_title("Antibiotic Resistance Results")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

    def get_statistics(self):
        diameters = self.data['Inhibition Zone Diameter (mm)'].values
        if len(diameters) == 0:
            return None, None, None
        mean = np.mean(diameters)
        std_np = np.std(diameters)
        std_scipy = np.sqrt(stats.tvar(diameters))  # sample variance
        return mean, std_np, std_scipy

    def compare_two_antibiotics(self, ab1, ab2):
        data_ab1 = self.data[self.data['Antibiotic'] == ab1]['Inhibition Zone Diameter (mm)']
        data_ab2 = self.data[self.data['Antibiotic'] == ab2]['Inhibition Zone Diameter (mm)']
        if len(data_ab1) < 2 or len(data_ab2) < 2:
            return None, None
        t_stat, p_val = stats.ttest_ind(data_ab1, data_ab2, equal_var=False)
        return t_stat, p_val


# ----------------- VIEW -----------------
class AntibiogramView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Antibiogram Result Analysis")
        self.geometry("800x700")

        self.antibiotic_label = ttk.Label(self, text="Antibiotic:")
        self.antibiotic_entry = ttk.Entry(self)

        self.diameter_label = ttk.Label(self, text="Inhibition Zone Diameter (mm):")
        self.diameter_entry = ttk.Entry(self)

        self.add_button = ttk.Button(self, text="Add Data", command=self.add_click)

        self.results_frame = ttk.LabelFrame(self, text="Results")
        self.results_text = tk.Text(self.results_frame, height=10, width=70)
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=self.results_scrollbar.set)

        self.graph_frame = ttk.LabelFrame(self, text="Graph")
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.widget = self.canvas.get_tk_widget()

        self.update_button = ttk.Button(self, text="Update Graph", command=self.update_click)
        self.stats_button = ttk.Button(self, text="Show Statistics", command=self.controller.show_statistics)

        self.compare_label1 = ttk.Label(self, text="Antibiotic 1:")
        self.compare_entry1 = ttk.Entry(self)
        self.compare_label2 = ttk.Label(self, text="Antibiotic 2:")
        self.compare_entry2 = ttk.Entry(self)
        self.compare_button = ttk.Button(self, text="Compare Antibiotics", command=self.compare_click)

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
        self.stats_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.compare_label1.grid(row=7, column=0, padx=5, pady=2, sticky="w")
        self.compare_entry1.grid(row=7, column=1, padx=5, pady=2, sticky="ew")
        self.compare_label2.grid(row=8, column=0, padx=5, pady=2, sticky="w")
        self.compare_entry2.grid(row=8, column=1, padx=5, pady=2, sticky="ew")
        self.compare_button.grid(row=9, column=0, columnspan=2, pady=5)

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
        self.results_text.insert(tk.END, results_df.to_string(index=False))

    def update_graph(self):
        self.controller.update_graph(self.axes)
        self.canvas.draw()

    def update_click(self):
        self.controller.update_results()

    def compare_click(self):
        ab1 = self.compare_entry1.get()
        ab2 = self.compare_entry2.get()
        if not ab1 or not ab2:
            tkinter.messagebox.showerror("Error", "Please enter two antibiotic names.")
            return
        self.controller.show_comparison(ab1, ab2)


# ----------------- CONTROLLER -----------------
class AntibiogramController:
    def __init__(self):
        self.model = AntibiogramModel()
        self.view = AntibiogramView(self)

    def add_data(self, antibiotic, diameter):
        if self.model.add_data(antibiotic, diameter):
            self.update_results()
        else:
            tkinter.messagebox.showerror("Error", "Invalid diameter value entered.")

    def update_results(self):
        results = self.model.get_results()
        self.view.update_results_text(results)
        self.update_graph(self.view.axes)

    def update_graph(self, ax):
        self.model.create_graph(ax)
        self.view.canvas.draw()

    def show_statistics(self):
        mean, std_np, std_scipy = self.model.get_statistics()
        if mean is None:
            tkinter.messagebox.showinfo("Statistics", "No data available.")
        else:
            msg = (f"Mean Diameter: {mean:.2f} mm\n"
                   f"Standard Deviation (NumPy): {std_np:.2f} mm\n"
                   f"Standard Deviation (SciPy): {std_scipy:.2f} mm")
            tkinter.messagebox.showinfo("Statistics", msg)

    def show_comparison(self, ab1, ab2):
        t_stat, p_val = self.model.compare_two_antibiotics(ab1, ab2)
        if t_stat is None:
            tkinter.messagebox.showinfo("Comparison", "Not enough data to compare.")
        else:
            msg = f"T-test statistic: {t_stat:.3f}\nP-value: {p_val:.4f}"
            tkinter.messagebox.showinfo("Comparison", msg)

    def run(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = AntibiogramController()
    app.run()
