from django.test import TestCase
from director.supporting import write_csv_file, write_xlsx_file
from django.utils import timezone
from django.contrib.auth import get_user_model
from user.models import Department, Company, Project, Task
from datetime import date

import os
import csv
import pandas

User = get_user_model()

class SupportingTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.company = Company.objects.create(name="Abc")
        cls.department = Department.objects.create(name="abc", company=cls.company)
        cls.test_user = User.objects.create(password="", email="abc@mail.ru", role=3, is_superuser=True,
                                               first_name="abc", last_name="abc", is_staff=1, is_active=1,
                                               date_joined=timezone.now(), post="user", department=cls.department)
        cls.project = Project.objects.create(name="abc", company=cls.company)
        cls.task = Task.objects.create(date=date.today(), time_worked=120, description="abc",
                                       project=cls.project, user=cls.test_user)

    @classmethod
    def tearDownClass(cls):
        for elem in [cls.task, cls.project, cls.test_user, cls.department, cls.company]:
            elem.delete()

    def test_write_csv_file(self):
        with open("data.csv", "w") as file:
            write_csv_file({self.test_user: [self.task]}, file)
        self.assertTrue(os.path.isfile("data.csv"))
        data = ["First name;Last name;Date;Worked time;Name project;Description", f"abc;abc;{date.today()};120;abc;abc"]
        with open("data.csv", newline="") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                self.assertEqual(row[0], data[i])
        os.remove("data.csv")


    def test_write_xlsx_file(self):
        write_xlsx_file({self.test_user: [self.task]}, "data.xlsx")
        self.assertTrue(os.path.isfile("data.xlsx"))
        excel_data_df = pandas.read_excel("data.xlsx")
        self.assertEqual(excel_data_df["First name"].tolist()[0], "abc")
        self.assertEqual(excel_data_df["Last name"].tolist()[0], "abc")
        self.assertEqual(excel_data_df["Date"].tolist()[0], f"{date.today()}")
        self.assertEqual(excel_data_df["Worked time"].tolist()[0], 120)
        self.assertEqual(excel_data_df["Name project"].tolist()[0], "abc")
        self.assertEqual(excel_data_df["Description"].tolist()[0], "abc")
        os.remove("data.xlsx")