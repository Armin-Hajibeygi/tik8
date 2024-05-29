from datetime import datetime
from gsheet import Sheet
from const import gsheet_names
from messages import NOT_VALID_WORKSHEET_NAME, NO_TASKS_FOR_TODAY, NO_WORKSHEET_IN_SHEET


def connect_sheet(user_id: int) -> Sheet:
    """Connect to the Google Sheet for the given user ID."""
    return Sheet(gsheet_names[user_id])


def check_worksheet_availability(user_id: int, worksheet_name: str) -> str:
    """Check if the worksheet is available in the user's Google Sheet."""
    worksheet_name = worksheet_name.strip()
    sheet = connect_sheet(user_id)
    worksheet_names = sheet.get_all_worksheet_names()

    if any(name.lower() == worksheet_name.lower() for name in worksheet_names):
        return worksheet_name
    return NOT_VALID_WORKSHEET_NAME


def get_today_tasks(user_id: int, input_worksheet_name: str) -> str:
    """Retrieve tasks for today from the specified worksheets."""
    sheet = connect_sheet(user_id)
    worksheets = (
        input_worksheet_name.split("-") if input_worksheet_name else sheet.get_all_worksheet_names()
    )
    response_parts = []

    for worksheet in worksheets:
        worksheet_name = check_worksheet_availability(user_id, worksheet)
        if worksheet_name == NOT_VALID_WORKSHEET_NAME:
            response_parts.append(NOT_VALID_WORKSHEET_NAME)
        else:
            response_parts.append(get_single_worksheet_tasks(sheet, worksheet_name))
        response_parts.append("\n------\n")

    return ''.join(response_parts)


def get_single_worksheet_tasks(sheet: Sheet, worksheet_name: str) -> str:
    """Retrieve tasks for today from a single worksheet."""
    sheet.create_df(worksheet_name)
    today = datetime.today().strftime("%d %b").lstrip("0").replace(" 0", " ")

    tasks = [
        f"<b>{worksheet_name}</b> - Lesson <u>{index}</u> for the <u>{column}</u> time"
        for index, row in sheet.df.iterrows()
        for column in sheet.df.columns
        if row[column] == today
    ]

    return "\n".join(tasks) if tasks else NO_TASKS_FOR_TODAY


def get_all_lessons(user_id: int) -> str:
    """Retrieve all lessons from the user's Google Sheet."""
    sheet = connect_sheet(user_id)
    worksheet_names = sheet.get_all_worksheet_names()

    return "\n".join(worksheet_names) if worksheet_names else NO_WORKSHEET_IN_SHEET
