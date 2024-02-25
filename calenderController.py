from calendarModel import Event
from datetime import datetime, timedelta

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
        self.events_manager.load_events_from_google()
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
    def __init__(self,google_events):
        self.google_events=google_events
        self.google_events_list=[]
        self.allEvents=[]
        self.events = []  # Initialize an empty list to store events

    def load_events_from_google(self):
        for e in self.google_events:
            event_name = e.get('summary', 'No Name')
            start_time = e['start'].get('dateTime', e['start'].get('date'))
            date = start_time.split('T')[0]  # Extract date part
            time = start_time.split('T')[1][:5]  # Extract time part (HH:MM format)
            duration = self.calculate_event_duration(e['start'], e['end'])
            newEvent=Event(event_name,date,time,duration)
            self.google_events_list.append(newEvent)

        self.allEvents = self.events+self.google_events_list

    def parse_time(self, time_string):
        if 'T' in time_string:
            # Split the string into date and time parts
            date_part, time_part = time_string.split('T')

            # Extract the timezone offset if present
            if '+' in time_part:
                time_part, timezone_offset = time_part.split('+')
                timezone_sign = '+'
            elif '-' in time_part:
                time_part, timezone_offset = time_part.split('-')
                timezone_sign = '-'
            else:
                timezone_offset = None

            # Convert the date and time parts to datetime objects
            date_obj = datetime.strptime(date_part, '%Y-%m-%d')
            time_obj = datetime.strptime(time_part, '%H:%M:%S')

            # If timezone offset is present, adjust the time accordingly
            if timezone_offset:
                hours, minutes = timezone_offset.split(':')
                hours = int(hours)
                minutes = int(minutes)
                timezone_delta = timedelta(hours=hours, minutes=minutes)
                if timezone_sign == '-':
                    timezone_delta = -timezone_delta
                time_obj += timezone_delta

            # Combine the date and time objects
            return date_obj.replace(hour=time_obj.hour, minute=time_obj.minute, second=time_obj.second)
        else:
            return datetime.strptime(time_string, '%Y-%m-%d')
    def calculate_event_duration(self,start, end):
        start_time =self.parse_time(start.get('dateTime', start.get('date')))
        end_time = self.parse_time(end.get('dateTime', end.get('date')))
        duration = end_time - start_time
        return duration.total_seconds() / 3600  # Convert seconds to hours


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
