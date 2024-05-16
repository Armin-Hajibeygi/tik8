import gspread
import pandas as pd
from const import gsheet_name
from datetime import datetime


class Sheet:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.client = gspread.service_account(filename="client_secret.json")
        self.sheet_id = self.get_sheet_id()
        self.sheet = self.client.open(self.sheet_name).get_worksheet_by_id(
            self.sheet_id
        )
        self.df = None
        self.data = None
        self.create_df()

    def get_sheet_id(self):
        sheets = self.client.open(self.sheet_name).worksheets()
        return sheets[-1].id

    def create_df(self):
        self.data = self.sheet.get_all_values()
        self.df = pd.DataFrame(self.data[1:], columns=self.data[0]).set_index(
            self.data[0][0]
        )


if __name__ == "__main__":
    sheet = Sheet(gsheet_name)
    sheet_df = sheet.df

    today = datetime.today().strftime("%d %b").lstrip("0").replace(" 0", " ")
    tasks = [
        f"Lesson {index} for the {column} time"
        for index, row in sheet.df.iterrows()
        for column in sheet.df.columns
        if row[column] == today
    ]
    text = "\n".join(tasks) if tasks else "You have no other tasks for today!"

    print(text)
