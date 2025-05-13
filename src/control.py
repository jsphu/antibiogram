# Controller.py
from src.model import AntibiogramModel
from src.view import AntibiogramView
import tkinter.messagebox

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
        self.view.canvas.draw()

    def update_graph(self, ax):
        self.model.create_graph(ax)

    def run(self):
        self.view.mainloop()