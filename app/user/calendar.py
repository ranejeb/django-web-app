from datetime import date
from calendar import monthrange
from holidays import Belarus

years = [year for year in range(date.today().year, 2009, -1)]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Day:
    """Класс, описывающий день"""
    def __init__(self, num: int, is_working_day: bool = True):
        self.num, self.is_working_day = num, is_working_day

    def __str__(self):
        return f"Day: {self.num} - {'workday' if self.is_working_day else 'weekend'}"

    def __repr__(self):
        return self.__str__()


def get_public_holidays(year: int, month: int) -> list:
    """Получаем праздничные дни в Республике Беларусь"""
    return [elem[0].day for elem in Belarus(years=year).items() if elem[0].month == month]


def get_all_weeks_month(year: int, month: int) -> list:
    """Распределяет дни месяца по неделям"""
    days = [Day(num, False if date(year, month, num).weekday() in [5, 6] or num in get_public_holidays(year, month)
                else True) for num in range(1, monthrange(year, month)[1] + 1)]

    day_week = date(year, month, 1).weekday()
    weeks = [[None for i in range(0, day_week)] + [days.pop(0) for _ in range(day_week, 7)]]

    while len(days) != 0:
        weeks.append(days[:7])
        del days[:7]

    return weeks
