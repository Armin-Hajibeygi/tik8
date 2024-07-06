from datetime import datetime, timedelta
from gsheet import Sheet
from const import gsheet_names
from messages import NOT_VALID_WORKSHEET_NAME, NO_TASKS_FOR_TODAY, NO_WORKSHEET_IN_SHEET

# Define the mapping from abbreviated month names to full month names
MONTH_MAP = {
    "Jan": "January",
    "Feb": "February",
    "Mar": "March",
    "Apr": "April",
    "May": "May",
    "Jun": "June",
    "Jul": "July",
    "Aug": "August",
    "Sep": "September",
    "Oct": "October",
    "Nov": "November",
    "Dec": "December",
}


def connect_sheet(user_id: int) -> Sheet:
    """Connect to the Google Sheet for the given user ID."""
    return Sheet(gsheet_names[user_id])


def check_worksheet_availability(user_id: int, worksheet_name: str) -> str:
    """Check if the worksheet is available in the user's Google Sheet."""
    worksheet_name = worksheet_name.strip()
    sheet = connect_sheet(user_id)
    worksheet_names = sheet.get_all_worksheet_names()

    for name in worksheet_names:
        if name.lower() == worksheet_name.lower():
            return name
    return NOT_VALID_WORKSHEET_NAME


def get_dates(date: str) -> (str, str):
    """Get today's date in both abbreviated and full month name formats."""
    if date == "today":
        abbr_date = datetime.today().strftime("%d %b").lstrip("0").replace(" 0", " ")
    elif date == "tomorrow":
        tomorrow_date = datetime.today() + timedelta(days=1)
        abbr_date = tomorrow_date.strftime("%d %b").lstrip("0").replace(" 0", " ")

    day, abbr_month = abbr_date.split()
    full_month = MONTH_MAP[abbr_month]
    full_date = f"{day} {full_month}"

    return abbr_date, full_date


def get_day_tasks(user_id: int, input_worksheet_name: str, date: str) -> str:
    """Retrieve tasks for day from the specified worksheets."""
    sheet = connect_sheet(user_id)
    worksheets = (
        input_worksheet_name.split("-")
        if input_worksheet_name
        else sheet.get_all_worksheet_names()
    )
    response_parts = []

    for worksheet in worksheets:
        worksheet_name = check_worksheet_availability(user_id, worksheet)
        if worksheet_name == NOT_VALID_WORKSHEET_NAME:
            response_parts.append(NOT_VALID_WORKSHEET_NAME)
        else:
            response_parts.append(
                get_single_worksheet_tasks(sheet, worksheet_name, date)
            )
        response_parts.append("\n------\n")

    return "".join(response_parts)


def get_single_worksheet_tasks(sheet: Sheet, worksheet_name: str, date: str) -> str:
    """Retrieve tasks for today from a single worksheet."""
    sheet.create_df(worksheet_name)
    abbr_date, full_date = get_dates(date)

    tasks = [
        f"Lesson <u>{index}</u> for the <u>{column}</u> time"
        for index, row in sheet.df.iterrows()
        for column in sheet.df.columns
        if row[column] == abbr_date or row[column] == full_date
    ]

    response = f"<b>{worksheet_name}</b>: \n"
    response += "\n".join(tasks) if tasks else NO_TASKS_FOR_TODAY

    return response


def get_all_lessons(user_id: int) -> str:
    """Retrieve all lessons from the user's Google Sheet."""
    sheet = connect_sheet(user_id)
    worksheet_names = sheet.get_all_worksheet_names()

    return "\n".join(worksheet_names) if worksheet_names else NO_WORKSHEET_IN_SHEET
