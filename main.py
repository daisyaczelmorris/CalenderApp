import tkinter as tk

from calendarModel import Calendar
from calendarView import CalendarView
from calenderController import CalendarController, EventsManager
import sys

from dayController import DayController
from dayModel import DayModel
from dayView import DayView

sys.path.append("..")  # Add parent folder to sys.path
from checkinggoogle.main import main as google

def main():
    calendar = Calendar()
    google_events = google()

    events_manager = EventsManager(google_events)
    root = tk.Tk()
    calendar_view = CalendarView(root, calendar, events_manager)
    day_model=DayModel()
    day_controller = DayController(day_model,calendar_view)

    calendar_controller = CalendarController(calendar, calendar_view, events_manager)

    file_name = "events_data.txt"  # File name to save/load events
    calendar_controller.load_events(file_name)  # Load events when the application starts

    calendar_view.set_controller(calendar_controller)

    root.mainloop()
    calendar_controller.save_events(file_name)


if __name__ == "__main__":
    main()
