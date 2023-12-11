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
    def __init__(self, root, calendar, events_manager):
        self.root = root
        self.calendar = calendar
        self.controller = None
        self.root.title("Calendar Display")
        self.events_manager = events_manager

        self.current_date = datetime.now()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.display_calendar()
    def add_event_popup(self):
        event_window = tk.Toplevel(self.root)
        event_window.title("Add Event")

        name_label = tk.Label(event_window, text="Event Name:")
        name_label.pack()
        name_entry = tk.Entry(event_window)
        name_entry.pack()

        date_label = tk.Label(event_window, text="Date (YYYY-MM-DD):")
        date_label.pack()
        date_entry = tk.Entry(event_window)
        date_entry.pack()

        time_label = tk.Label(event_window, text="Start Time (HH:MM):")
        time_label.pack()
        time_entry = tk.Entry(event_window)
        time_entry.pack()

        duration_label = tk.Label(event_window, text="Duration (hours):")
        duration_label.pack()
        duration_entry = tk.Entry(event_window)
        duration_entry.pack()

        add_button = tk.Button(event_window, text="Add", command=lambda: self.add_event(name_entry.get(), date_entry.get(), time_entry.get(), duration_entry.get(), event_window))
        add_button.pack()

    def add_event(self, name, date, start_time, duration, window):
        if name and date and start_time and duration:
            # Call controller function to add the event
            self.controller.add_event(name, date, start_time, duration)
            window.destroy()
            self.refresh_calendar()  # Refresh the calendar to display the newly added event
    def set_controller(self, controller):
        self.controller = controller
        self.prev_month_button = tk.Button(self.root, text="Previous Month", command=self.controller.prev_month)
        self.prev_month_button.pack(side=tk.LEFT)

        self.next_month_button = tk.Button(self.root, text="Next Month", command=self.controller.next_month)
        self.next_month_button.pack(side=tk.RIGHT)

        self.prev_year_button = tk.Button(self.root, text="Previous Year", command=self.controller.prev_year)
        self.prev_year_button.pack(side=tk.LEFT)

        self.next_year_button = tk.Button(self.root, text="Next Year", command=self.controller.next_year)
        self.next_year_button.pack(side=tk.RIGHT)

        self.add_event_button = tk.Button(self.root, text="Add Event", command=self.add_event_popup)
        self.add_event_button.pack(side=tk.RIGHT)
        #set button for add event set pop up for add event

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
                        label_events = tk.Label(date_box, text=event_texts, justify=tk.LEFT, wraplength=110,
                                                font=("Arial", 10))
                        label_events.pack(pady=5)

    def get_events_for_date(self, date):
        return [event for event in self.events_manager.events if event.date == date]

    def refresh_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        self.display_calendar()


class CalendarController:
    def __init__(self, calendar, view, event_manager):
        self.calendar = calendar
        self.view = view
        self.events_manager = event_manager
    def add_event(self,name,date,start_time,duration):{

        self.events_manager.create_event(name,date,start_time,duration)
    }
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
    # Create instances of the models
    calendar = Calendar()
    events_manager = EventsManager()

    # Create instances of the view and controller
    root = tk.Tk()
    calendar_view = CalendarView(root, calendar, events_manager)
    calendar_controller = CalendarController(calendar, calendar_view, events_manager)

    # Set the view's controller
    calendar_view.set_controller(calendar_controller)
    # Initialize the GUI and start the application
    root.mainloop()


if __name__ == "__main__":
    main()
