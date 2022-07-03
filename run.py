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
favouritesCells = {
    'Strategy': 'B2',
    'RPG': 'B3',
    'FPS (First Person Shooter)': 'B4',
    'Action': 'B5',
    'TPS (Third Person Shooter)': 'B6',
    'Simulation': 'B7',
    'Platformer': 'B8',
    'Adventure': 'B9',
    'Sport': 'B10'
}
leastCells = {
    'Strategy': 'C2',
    'RPG': 'C3',
    'FPS (First Person Shooter)': 'C4',
    'Action': 'C5',
    'TPS (Third Person Shooter)': 'C6',
    'Simulation': 'C7',
    'Platformer': 'C8',
    'Adventure': 'C9',
    'Sport': 'C10'
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
    tallies = SHEET.worksheet('Response tally')
    answers = tallies.get_all_values()
    print(answers[1])
    for array in data:
        for i in range(len(array)):
            if array[i] == ('Mobile' or 'PC' or 'Console'):
                continue
            answer = responseAnswers[array[i]]
            tally = int(answers[answer][i+1])
            tally = tally + 1
            if i == 0:
                tallies.update(favouritesCells[array[i]], tally)
            elif i == 1:
                tallies.update(leastCells[array[i]], tally)


results = get_responses()
calculate_response_tally(results)
