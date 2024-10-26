import tkinter  as tk
from datetime import datetime, timedelta

from dayModel import DayModel


class PeriodTracker:
    def __init__(self, start_date, cycle_length=28, menstrual_length=5, follicular_length=9, ovulatory_length=4,
                 luteal_length=10):
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.cycle_length = cycle_length
        self.menstrual_length = menstrual_length
        self.follicular_length = follicular_length
        self.ovulatory_length = ovulatory_length
        self.luteal_length = luteal_length

    def get_phase(self, date):
        days_since_start = (date - self.start_date).days % self.cycle_length

        if days_since_start < self.menstrual_length:
            return "Menstrual"
        elif days_since_start < self.menstrual_length + self.follicular_length:
            return "Follicular"
        elif days_since_start < self.menstrual_length + self.follicular_length + self.ovulatory_length:
            return "Ovulatory"
        else:
            return "Luteal"

class CalendarView:
    def __init__(self, root, calendar, events_manager):
        self.root = root
        self.calendar = calendar
        self.controller = None
        self.root.title("Calendar Display")
        self.dayModel=DayModel()


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
          #  window.destroy()
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



    def display_calendar(self):
        days_in_month = self.calendar.days_in_month(self.current_year, self.current_month)
        first_day = datetime(self.current_year, self.current_month, 1)
        weekday = first_day.weekday()

        # PeriodTracker setup (example start date: October 12, 2024)
        period_tracker = PeriodTracker(start_date="2024-10-12")
        # Create labels for displaying year, month, and days of the week
        year_label = tk.Label(self.calendar_frame, text=f"{self.current_year}", font=("Arial", 16))
        year_label.grid(row=0, column=0, columnspan=8, sticky="nsew")

        month_label = tk.Label(self.calendar_frame, text=f"{first_day.strftime('%B')}", font=("Arial", 14))
        month_label.grid(row=1, column=0, columnspan=8, sticky="nsew")

        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            label_day = tk.Label(self.calendar_frame, text=day, font=("Arial", 12))
            label_day.grid(row=2, column=i, sticky="nsew")

        # Determine the width and height of each cell
        cell_width = 150
        cell_height = 100

        # Configure grid layout to ensure all cells are the same size
        for i in range(6):  # Rows
            self.calendar_frame.grid_rowconfigure(i + 3, minsize=cell_height)
        for i in range(7):  # Columns
            self.calendar_frame.grid_columnconfigure(i, minsize=cell_width)

        # Display calendar days
        for row in range(6):  # Assuming maximum 6 rows for a month layout
            for col in range(7):
                day_number = (row * 7) + col + 1 - weekday

                if 1 <= day_number <= days_in_month:
                    date_text = f"{self.current_year}-{self.current_month:02d}-{day_number:02d}"
                    date_box = tk.Frame(self.calendar_frame, width=cell_width, height=cell_height, borderwidth=1,
                                        relief="solid")
                    date_box.grid(row=row + 3, column=col, padx=5, pady=5, sticky="nsew")  # Adjust row index for days

                    # Label to display the date
                    label_date = tk.Label(date_box, text=f"{day_number}", font=("Arial", 12),
                                          wraplength=cell_width - 10)
                    label_date.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

                    # Determine the current date and the phase
                    current_date = datetime(self.current_year, self.current_month, day_number)
                    phase = period_tracker.get_phase(current_date)

                    # Label to display period phase
                    if phase:
                        label_phase = tk.Label(date_box, text=f"{phase}", justify=tk.LEFT, wraplength=cell_width - 10,
                                               font=("Arial", 10))
                        label_phase.grid(row=1, column=0, sticky="nw", padx=5, pady=5)

                    # Label to display events (if any)
                    events_on_day = self.get_events_for_date(date_text)
                    if events_on_day:
                        event_texts = "\n".join([f"{event.name}" for event in events_on_day])
                        label_events = tk.Label(date_box, text=event_texts, justify=tk.LEFT, wraplength=cell_width - 10,
                                                font=("Arial", 10))
                        label_events.grid(row=2, column=0, sticky="nw", padx=5, pady=5)

                    # Bind click event to the date box
                    date_box.bind("<Button-1>", lambda event, date=date_text: self.on_date_clicked(date))
        # Create spare container for future development
        self.spare_container = tk.Frame(self.calendar_frame, width=cell_width, height=cell_height, borderwidth=1,
                                   relief="solid")
        self.spare_container.grid(row=3, column=7, rowspan=6, padx=5, pady=5, sticky="nsew")

    def get_events_for_date(self, date):
        return [event for event in self.events_manager.allEvents if event.date == date]

    def refresh_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        self.display_calendar()
    def on_date_clicked(self,date):
        self.dayModel.events=[]
        self.dayModel.date=date
        for e in self.events_manager.allEvents:
            if e.date==date:
                self.dayModel.events.append(e)
        self.dayModel.update()
        self.show_day()

    def show_day(self):
        self.refresh_calendar()
        day_label = tk.Label(self.spare_container, text=f"{self.dayModel.date}", font=("Arial", 16))
        day_label.pack()
        print(self.dayModel.schedule)
        for k, v in self.dayModel.schedule.items():
            print(v)
            if len(v)==0:
                day_label = tk.Label(self.spare_container, text=f"{k}", font=("Arial", 10))
                day_label.pack(anchor="w")
            else:
                string=""
                for event in v:
                    string+=event.name
                day_label = tk.Label(self.spare_container, text=f"{k}"+": "+string, font=("Arial", 10))
                day_label.pack(anchor="w")






