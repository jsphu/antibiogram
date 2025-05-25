# Model.py
import sys
import os
import pandas as pd
import numpy as np
from scipy import stats

class AntibiogramModel:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Antibiotic', 'Inhibition Zone Diameter (mm)'])
        self.resistance_thresholds = self.load_resistance_thresholds()
    
    # Get absolute path to resource, implemented for windows-like systems.
    def resource_path(self, relative_path):
        """ Get absolute path to resource (works for dev and PyInstaller) """
        try:
            base_path = sys._MEIPASS  # PyInstaller sets this in the temp folder
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def add_data(self, antibiotic, diameter):
        try:
            diameter = float(diameter)
            new_row = pd.DataFrame([{'Antibiotic': antibiotic, 'Inhibition Zone Diameter (mm)': diameter}])
            self.data = pd.concat([self.data, new_row], ignore_index=True)
            return True
        except ValueError:
            return False

    def interpret_resistance(self, diameter, antibiotic):
        if antibiotic in self.resistance_thresholds:
            thresholds = self.resistance_thresholds[antibiotic]
            # Use the CSV column names: Susceptible, Intermediate, Resistant
            if diameter >= thresholds['Susceptible']:
                return "Susceptible"
            elif thresholds['Intermediate'] <= diameter < thresholds['Susceptible']:
                return "Intermediate"
            else:
                return "Resistant"
        else:
            return "No Threshold Data"

    def load_resistance_thresholds(self):
        with open(self.resource_path("data/antibiotics.csv"), "r") as file:
            return pd.read_csv(file, index_col='Antibiotic').to_dict(orient='index')

    def get_results(self):
        results = []
        for _, row in self.data.iterrows():
            antibiotic = row['Antibiotic']
            measured_diameter = row['Inhibition Zone Diameter (mm)']
            interpretation = self.interpret_resistance(measured_diameter, antibiotic)
            results.append({
                'Antibiotic': antibiotic,
                'Diameter': measured_diameter,
                'Result': interpretation
            })
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
    
    def load_bacteria_antibiotic_resistance(self):
        return pd.read_csv(self.resource_path("data/bacterias.csv"))

    def evaluate_bacteria(self):
        # Use the results computed (which include the interpretation) from the user's data.
        results_df = self.get_results()
        if results_df.empty:
            return "No measurement data available."

        # Build a dictionary mapping antibiotic to its measured result letter (S, I, or R)
        measured = {}
        for _, row in results_df.iterrows():
            # Take only the first letter of the interpretation.
            measured[row['Antibiotic']] = row['Result'][0].upper()

        # Load bacterial data from CSV.
        bacteria_df = self.load_bacteria_antibiotic_resistance()
        scores = {}

        # Evaluate each unique bacterium.
        for bact in bacteria_df['Bacteria'].unique():
            scores[bact] = 0
            b_data = bacteria_df[bacteria_df['Bacteria'] == bact]
            # For each antibiotic measured by the user, check if the bacteria reaction matches.
            for ab, measured_res in measured.items():
                matching = b_data[b_data['Antibiotic'] == ab]
                if not matching.empty:
                    reaction = matching.iloc[0]['Reaction'].upper()
                    if reaction == measured_res:
                        scores[bact] += 1

        if not scores:
            return "No matching bacteria data found."

        # Select the bacterium with the highest match score.
        best_bacterium = max(scores, key=lambda k: scores[k])
        best_score = scores[best_bacterium]

        if best_score == 0:
            return "Not enough data to determine a matching bacterium."
        
        if best_score <= 2:
            return f"The best matching bacteria is: {best_bacterium} \nThis is not a perfect score. Use with caution.\n(match score: {best_score})"
        
        return f"The best matching bacteria is: {best_bacterium} \n(match score: {best_score})"
    
    def clear_data(self) -> None:
        self.data = pd.DataFrame(columns=['Antibiotic', 'Inhibition Zone Diameter (mm)'])