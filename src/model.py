# Model.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AntibiogramModel:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Antibiotic', 'Inhibition Zone Diameter (mm)'])
        self.resistance_thresholds = {
            'Penicillin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
            'Cefazolin': {'susceptible': 18, 'intermediate': 15, 'resistant': 14},
            'Erythromycin': {'susceptible': 18, 'intermediate': 14, 'resistant': 13},
            'Tetracycline': {'susceptible': 19, 'intermediate': 15, 'resistant': 14},
            'Gentamicin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
            # Add more antibiotics and threshold values
        }

    def add_data(self, antibiotic, diameter):
        try:
            diameter = float(diameter)
            self.data = pd.concat([self.data, pd.DataFrame([{'Antibiotic': antibiotic, 'Inhibition Zone Diameter (mm)': diameter}])], ignore_index=True)
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
        for index, row in self.data.iterrows():
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
        ax.bar(antibiotics, diameters)
        ax.set_xlabel("Antibiotic")
        ax.set_ylabel("Inhibition Zone Diameter (mm)")
        ax.set_title("Antibiotic Resistance Results")
        ax.tick_params(axis='x', rotation=45, ha='right')
        plt.tight_layout()