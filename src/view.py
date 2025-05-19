# View.py
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk

class AntibiogramView(ctk.CTk):
    def __init__(self, controller, antibiotics):
        super().__init__()
        self.controller = controller
        self.title("Antibiogram Analysis App")
        self.geometry("850x650")

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.antibiotic_label = ctk.CTkLabel(self, text="Select Antibiotic:")
        self.antibiotic_options = list(controller.model.resistance_thresholds.keys())
        self.antibiotic_var = ctk.StringVar(value=self.antibiotic_options[0])
        self.antibiotic_menu = ctk.CTkOptionMenu(self, values=self.antibiotic_options, variable=self.antibiotic_var)

        self.diameter_label = ctk.CTkLabel(self, text="Inhibition Zone Diameter (mm):")
        self.diameter_entry = ctk.CTkEntry(self)

        self.add_button = ctk.CTkButton(self, text="Add Data", command=self.add_click)

        self.antibiotic_label.pack(pady=5)
        self.antibiotic_menu.pack(pady=5)

        self.diameter_entry.pack(pady=10)
        self.add_button.pack(pady=5)

        self.result_box = ctk.CTkTextbox(self, height=150)
        self.result_box.pack(pady=10, fill='both', expand=False)

        self.stats_button = ctk.CTkButton(self, text="Show Statistics", command=self.controller.show_statistics)
        self.stats_button.pack(pady=5)

        self.popup_button = ctk.CTkButton(self, text="Pop-out Graph Window", command=self.controller.show_graph_popup)
        self.popup_button.pack(pady=10)

        self.compare_frame = ctk.CTkFrame(self)
        self.compare_frame.pack(pady=10)

        self.compare_entry1 = ctk.CTkEntry(self.compare_frame, placeholder_text="Antibiotic 1")
        self.compare_entry2 = ctk.CTkEntry(self.compare_frame, placeholder_text="Antibiotic 2")
        self.compare_button = ctk.CTkButton(self.compare_frame, text="Compare", command=self.compare_click)

        self.compare_entry1.pack(side="left", padx=5)
        self.compare_entry2.pack(side="left", padx=5)
        self.compare_button.pack(side="left", padx=5)

    def add_click(self):
        antibiotic = self.antibiotic_var.get()
        diameter = self.diameter_entry.get()
        self.controller.add_data(antibiotic, diameter)
        self.diameter_entry.delete(0, tk.END)

    def update_results_text(self, results_df):
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", results_df.to_string(index=False))

    def compare_click(self):
        ab1 = self.compare_entry1.get()
        ab2 = self.compare_entry2.get()
        if not ab1 or not ab2:
            tkinter.messagebox.showerror("Error", "Please enter two antibiotic names.")
            return
        self.controller.show_comparison(ab1, ab2)
