from django.test import TestCase
from datetime import date
from user.calendar import Day, years, get_public_holidays, get_all_weeks_month


def get_weekend_and_workday(weeks):
    weekend, workday = list(), list()
    for week in weeks:
        for day in week:
            if day is not None:
                if day.is_working_day:
                    workday.append(day)
                else:
                    weekend.append(day)
    return weekend, workday


class CalendarTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.today = date.today()

    @classmethod
    def tearDownClass(cls):
        pass

    def test_checks_years(self):
        self.assertIn(self.today.year, years)
        self.assertIn(2010, years)
        self.assertNotIn(self.today.year + 1, years)
        self.assertNotIn(2009, years)

    def test_1_checking_dunder_str_method_day_class(self):
        self.assertEqual(str(Day(self.today.day, True)), f"Day: {self.today.day} - workday")

    def test_2_checking_dunder_str_method_day_class(self):
        self.assertEqual(str(Day(self.today.day, False)), f"Day: {self.today.day} - weekend")

    def test_1_checks_public_holidays(self):
        holidays = get_public_holidays(2021, 5)
        self.assertIn(1, holidays)
        self.assertIn(11, holidays)
        self.assertIn(9, holidays)

    def test_2_checks_public_holidays(self):
        holidays = get_public_holidays(2021, 4)
        self.assertEqual(len(holidays), 0)

    def test_1_checks_distribution_days_week(self):
        weeks = get_all_weeks_month(2021, 5)
        self.assertEqual(len(weeks), 6)
        weekend, workday = get_weekend_and_workday(weeks)
        self.assertEqual(len(weekend), 11)
        self.assertEqual(len(workday), 20)

    def test_2_checks_distribution_days_week(self):
        weeks = get_all_weeks_month(2021, 4)
        self.assertEqual(len(weeks), 5)
        weekend, workday = get_weekend_and_workday(weeks)
        self.assertEqual(len(weekend), 8)
        self.assertEqual(len(workday), 22)
