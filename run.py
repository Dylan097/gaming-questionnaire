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

responseAnswers = {
    'Strategy': 1,
    'RPG': 2,
    'FPS (First Person Shooter)': 3,
    'Action': 4,
    'TPS (Third Person Shooter)': 5,
    'Simulation': 6,
    'Platformer': 7,
    'Adventure': 8,
    'Sport': 9
}


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
    tally = SHEET.worksheet('Response tally')
    answers = tally.get_all_values()
    print(answers[1])
    for array in data:
        for i in range(len(array)):
            if array[i] == ('Mobile' or 'PC' or 'Console'):
                continue
            answer = responseAnswers[array[i]]
            print(answers[answer][i+1])


results = get_responses()
calculate_response_tally(results)
