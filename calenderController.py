from calendarModel import Event
class CalendarController:
    def __init__(self, calendar, view, event_manager):
        self.calendar = calendar
        self.view = view
        self.events_manager = event_manager
    def add_event(self,name,date,start_time,duration):{

        self.events_manager.create_event(name,date,start_time,duration)
    }

    def save_events(self, file_name):
        self.events_manager.save_events_to_file(file_name)

    def load_events(self, file_name):
        self.events_manager.load_events_from_file(file_name)
        self.view.refresh_calendar()  # Refresh the calendar view after loading events
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


class EventsManager:
    def __init__(self):
        self.events = []  # Initialize an empty list to store events

    def save_events_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for event in self.events:
                file.write(f"{event.name},{event.date},{event.time},{event.duration}\n")

    def load_events_from_file(self, file_name):
        self.events = []  # Clear existing events before loading from the file
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    event_data = line.strip().split(',')
                    if len(event_data) == 4:
                        name, date, time, duration = event_data
                        self.create_event(name, date, time, duration)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            with open(file_name, 'x') as file:
                for event in self.events:
                    file.write(f"{event.name},{event.date},{event.time},{event.duration}\n")
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
