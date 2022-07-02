import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('gaming_questionnaire')

responses = SHEET.worksheet('Responses')


def get_responses():
    """
    Collect the responses from the spreadsheet.
    Return the data for calculation for other spreadsheets
    """

    data = responses.get_all_values()
    for i in range(len(data)):
        data[i] = data[i][slice(1,4)]
    data = data[slice(1, (len(data)+1))]
    return data


def calculate_response_tally(data):
    """
    Gets each response made and calculates how many times
    the response was given
    """
    pprint(data)


results = get_responses()
calculate_response_tally(results)
