import tkinter as tk

from calendarModel import Calendar
from calendarView import CalendarView
from calenderController import CalendarController, EventsManager


def main():
    # Create instances of the models
    calendar = Calendar()
    events_manager = EventsManager()

    # Create instances of the view and controller
    root = tk.Tk()
    calendar_view = CalendarView(root, calendar, events_manager)
    calendar_controller = CalendarController(calendar, calendar_view, events_manager)

    file_name = "events_data.txt"  # File name to save/load events
    calendar_controller.load_events(file_name)  # Load events when the application starts

    # Set the view's controller
    calendar_view.set_controller(calendar_controller)
    # Initialize the GUI and start the application
    root.mainloop()
    calendar_controller.save_events(file_name)



if __name__ == "__main__":
    main()
