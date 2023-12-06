import tkinter as tk
from datetime import datetime, timedelta
class Event:
    def __init__(self, name, date, time, duration):
        self.name = name
        self.date = date
        self.time = time
        self.duration = duration

    def __str__(self):
        return f"Event: {self.name}\nDate: {self.date}\nTime: {self.time}\nDuration: {self.duration} hours"


class EventsManager:
    def __init__(self):
        self.events = []  # Initialize an empty list to store events

    def create_event(self, name, date, time, duration):
        new_event = Event(name, date, time, duration)
        self.events.append(new_event)
        return new_event

    def read_event(self, index):
        if 0 <= index < len(self.events):
            return self.events[index]
        return None

    def update_event(self, index, name=None, date=None, time=None, duration=None):
        if 0 <= index < len(self.events):
            event = self.events[index]
            if name:
                event.name = name
            if date:
                event.date = date
            if time:
                event.time = time
            if duration:
                event.duration = duration
            return event
        return None

    def delete_event(self, index):
        if 0 <= index < len(self.events):
            return self.events.pop(index)
        return None

    def list_events(self):
        return self.events

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
    def __init__(self, root, calendar, controller,eventsManager):
        self.root = root
        self.calendar = calendar
        self.controller = controller
        self.root.title("Calendar Display")
        self.events_manager=eventsManager


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

        for row in range(6):  # Assuming maximum 6 rows for a month layout
            for col in range(7):
                day_number = (row * 7) + col + 1 - weekday

                if 1 <= day_number <= days_in_month:
                    date_text = f"{self.current_year}-{self.current_month:02d}-{day_number:02d}"
                    date_box = tk.Frame(self.calendar_frame, width=120, height=120, borderwidth=1, relief="solid")
                    date_box.grid(row=row, column=col, padx=5, pady=5)

                    label_date = tk.Label(date_box, text=f"{day_number}", font=("Arial", 12))
                    label_date.pack(pady=20)

                    events_on_day = self.get_events_for_date(date_text)
                    if events_on_day:
                        event_texts = "\n".join([f"{event.name} - {event.time}" for event in events_on_day])
                        label_events = tk.Label(date_box, text=event_texts, justify=tk.LEFT, wraplength=110, font=("Arial", 10))
                        label_events.pack(pady=5)
    def get_events_for_date(self, date):
        return [event for event in self.events_manager.events if event.date == date]

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
        self.view.current_year -= 1
        self.view.refresh_calendar()

    def next_year(self):
        self.view.current_year += 1
        self.view.refresh_calendar()



def main():
    root = tk.Tk()
    calendar = Calendar()
    events_manager = EventsManager()
    # Create events
    events_manager.create_event("Meeting", "2023-12-25", "15:00", 2)
    events_manager.create_event("Party", "2023-12-31", "20:00", 4)
    controller = CalendarController(calendar, None)  # Pass view as None initially
    calendar_view = CalendarView(root, calendar, controller,events_manager)
    controller.view = calendar_view  # Set view in controller after creation

    root.mainloop()

if __name__ == "__main__":
    main()
