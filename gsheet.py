import gspread
import pandas as pd
from const import gsheet_names
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
