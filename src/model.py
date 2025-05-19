# Model.py
import pandas as pd
import numpy as np
from scipy import stats

class AntibiogramModel:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Antibiotic', 'Inhibition Zone Diameter (mm)'])
        self.resistance_thresholds = {
            'Penicillin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
            'Cefazolin': {'susceptible': 18, 'intermediate': 15, 'resistant': 14},
            'Erythromycin': {'susceptible': 18, 'intermediate': 14, 'resistant': 13},
            'Tetracycline': {'susceptible': 19, 'intermediate': 15, 'resistant': 14},
            'Gentamicin': {'susceptible': 15, 'intermediate': 13, 'resistant': 12},
            'Amoxicillin': {'susceptible': 17, 'intermediate': 14, 'resistant': 13},
            'Ciprofloxacin': {'susceptible': 21, 'intermediate': 16, 'resistant': 15},
            'Vancomycin': {'susceptible': 20, 'intermediate': 17, 'resistant': 16},
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
