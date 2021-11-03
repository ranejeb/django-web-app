import csv
import pandas

column_names = ["First name", "Last name", "Date", "Worked time", "Name project", "Description"]


def write_csv_file(array, file):
    """Записывает содержимое в csv файл"""
    writer = csv.writer(file, delimiter=";", lineterminator="\r")
    writer.writerow(column_names)
    for user, tasks in array.items():
        for task in tasks:
            writer.writerow([user.first_name, user.last_name, str(task.date), task.time_worked,
                            task.project.name, task.description])
    return file


def write_xlsx_file(array, file):
    """Записывает содержимое в xlsx файл"""
    data_frame = {column_name: list() for column_name in column_names}
    for user, tasks in array.items():
        for task in tasks:
            data_frame["First name"].append(user.first_name)
            data_frame["Last name"].append(user.last_name)
            data_frame["Date"].append(str(task.date))
            data_frame["Worked time"].append(task.time_worked)
            data_frame["Name project"].append(task.project.name)
            data_frame["Description"].append(task.description)
    pandas.DataFrame(data_frame).to_excel(file)
    return file