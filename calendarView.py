import tkinter  as tk

from datetime import datetime, timedelta

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

        add_button = tk.Button(event_window, text="Add",
                               command=lambda: self.add_event(name_entry.get(), date_entry.get(), time_entry.get(),
                                                              duration_entry.get(), event_window))
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
        # set button for add event set pop up for add event

    def display_calendar(self):
        days_in_month = self.calendar.days_in_month(self.current_year, self.current_month)
        first_day = datetime(self.current_year, self.current_month, 1)
        weekday = first_day.weekday()

        # Create labels for displaying year, month, and days of the week
        year_label = tk.Label(self.calendar_frame, text=f"{self.current_year}", font=("Arial", 16))
        year_label.grid(row=0, column=0, columnspan=7)

        month_label = tk.Label(self.calendar_frame, text=f"{first_day.strftime('%B')}", font=("Arial", 14))
        month_label.grid(row=1, column=0, columnspan=7)

        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            label_day = tk.Label(self.calendar_frame, text=day)
            label_day.grid(row=2, column=i)

        # Display calendar days
        for row in range(6):  # Assuming maximum 6 rows for a month layout
            for col in range(7):
                day_number = (row * 7) + col + 1 - weekday

                if 1 <= day_number <= days_in_month:
                    date_text = f"{self.current_year}-{self.current_month:02d}-{day_number:02d}"
                    date_box = tk.Frame(self.calendar_frame, width=120, height=120, borderwidth=1, relief="solid")
                    date_box.grid(row=row + 3, column=col, padx=5, pady=5)  # Adjust row index for days

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

