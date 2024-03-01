import tkinter as tk
class DayModel:
    def __init__(self):
        self.date=None
        self.events=[]
        self.hours = ["5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00",
                      "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
        self.schedule = {}  # Initialize an empty dictionary for the schedule

    def update(self):
        for hour in self.hours:
            self.schedule[hour] = []  # Initialize an empty list for each hour

            events_in_hour = [event for event in self.events if event.time[:2] == hour]
            self.schedule[hour] = events_in_hour
        






