import tkinter as tk
from dayModel import DayModel
class DayView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.model = DayModel()  # Replace SomeModel with your actual model
        self.display_selected_date()

    def display_selected_date(self):
        self.label = tk.Label(self, textvariable=self.model.selected_date)
        self.label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    def update_day(self, date):
        self.model.selected_date = date
        self.display_selected_date()
