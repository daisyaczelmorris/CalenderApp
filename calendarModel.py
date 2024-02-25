
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

class Event:
    def __init__(self, name, date, time, duration):
        self.name = name
        self.date = date
        self.time = time
        self.duration = duration

    def __str__(self):
        return f"Event: {self.name}\nDate: {self.date}\nTime: {self.time}\nDuration: {self.duration} hours"
