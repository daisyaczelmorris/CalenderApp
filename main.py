import tkinter as tk
from datetime import datetime, timedelta

class Calendar:
    def __init__(self):
        self.days_in_month_dict = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }

    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def days_in_year(self, year):
        if self.is_leap_year(year):
            return 366
        return 365

    def days_in_month(self, year, month):
        if month == 2 and self.is_leap_year(year):
            return 29
        return self.days_in_month_dict[month]

class CalendarView:
    def __init__(self, root, calendar, controller):
        self.root = root
        self.calendar = calendar
        self.controller = controller
        self.root.title("Calendar Display")

        self.current_date = datetime.now()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.display_calendar()

        self.prev_month_button = tk.Button(self.root, text="Previous Month", command=self.controller.prev_month)
        self.prev_month_button.pack(side=tk.LEFT)

        self.next_month_button = tk.Button(self.root, text="Next Month", command=self.controller.next_month)
        self.next_month_button.pack(side=tk.RIGHT)

        self.prev_year_button = tk.Button(self.root, text="Previous Year", command=self.controller.prev_year)
        self.prev_year_button.pack(side=tk.LEFT)

        self.next_year_button = tk.Button(self.root, text="Next Year", command=self.controller.next_year)
        self.next_year_button.pack(side=tk.RIGHT)

    def display_calendar(self):
        days_in_month = self.calendar.days_in_month(self.current_year, self.current_month)
        first_day = datetime(self.current_year, self.current_month, 1)
        weekday = first_day.weekday()

        row = 0
        col = weekday  # Start from the correct weekday

        for day in range(1, days_in_month + 1):
            label = tk.Label(self.calendar_frame, text=f"{self.current_year}-{self.current_month:02d}-{day:02d}")
            label.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def refresh_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        self.display_calendar()

class CalendarController:
    def __init__(self, calendar, view):
        self.calendar = calendar
        self.view = view

    def prev_month(self):
        self.view.current_month -= 1
        if self.view.current_month == 0:
            self.view.current_month = 12
            self.view.current_year -= 1
        self.view.refresh_calendar()


    def next_month(self):
        self.view.current_month += 1
        if self.view.current_month == 13:
            self.view.current_month = 1
            self.view.current_year += 1
        self.view.refresh_calendar()

    def prev_year(self):
        self.current_year -= 1
        self.refresh_calendar()

    def next_year(self):
        self.current_year += 1
        self.refresh_calendar()



def main():
    root = tk.Tk()
    calendar = Calendar()
    controller = CalendarController(calendar, None)  # Pass view as None initially
    calendar_view = CalendarView(root, calendar, controller)
    controller.view = calendar_view  # Set view in controller after creation
    root.mainloop()

if __name__ == "__main__":
    main()
