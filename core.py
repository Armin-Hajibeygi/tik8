from datetime import datetime

from gsheet import Sheet
from const import gsheet_names


def connect_sheet(user_id: int):
    sheet = Sheet(gsheet_names[user_id])
    return sheet


def get_today_tasks(user_id: int, sheet_name=None):
    sheet = connect_sheet(user_id=user_id)

    today = datetime.today().strftime("%d %b").lstrip("0").replace(" 0", " ")
    tasks = [
        f"Lesson <u>{index}</u> for the <u>{column}</u> time"
        for index, row in sheet.df.iterrows()
        for column in sheet.df.columns
        if row[column] == today
    ]
    text = "\n".join(tasks) if tasks else "You have no other tasks for today!"

    return text
