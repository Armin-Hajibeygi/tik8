import gspread
import pandas as pd


class Sheet:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.client = gspread.service_account(filename="client_secret.json")
        self.worksheet = None
        self.worksheet_names = None
        self.df = None
        self.data = None

    def get_worksheet_by_name(self, worksheet_name):
        self.worksheet = self.client.open(self.sheet_name).worksheet(worksheet_name)

    def create_df(self, worksheet: str):
        self.get_worksheet_by_name(worksheet)
        self.data = self.worksheet.get_all_values()
        self.df = pd.DataFrame(self.data[1:], columns=self.data[0]).set_index(
            self.data[0][0]
        )

    def get_all_worksheet_names(self):
        self.worksheet_names = []
        for sheet in self.client.open(self.sheet_name).worksheets():
            self.worksheet_names.append(sheet.title)

        return self.worksheet_names
