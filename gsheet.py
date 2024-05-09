import gspread
from const import gsheet_name


class Sheet:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.client = gspread.service_account(filename="client_secret.json")
        self.sheet_id = self.get_sheet_id()
        self.sheet = self.client.open(self.sheet_name).get_worksheet_by_id(
            self.sheet_id
        )

    def get_sheet_id(self):
        sheets = self.client.open(self.sheet_name).worksheets()
        return sheets[-1].id
