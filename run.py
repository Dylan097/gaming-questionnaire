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

RESPONSES = SHEET.worksheet('Responses')
COMPLETED = SHEET.worksheet('Completed')
TALLIES = SHEET.worksheet('Response tally')

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
platformChoices = {
    'Mobile': 0,
    'PC': 1,
    'Console': 2
}
platformCells = {
    'Mobile': 'B1',
    'PC': 'B2',
    'Console': 'B3'
}
tallyCells = {
    'Strategy': 'B1',
    'RPG': 'B2',
    'FPS': 'B3',
    'Action': 'B4',
    'TPS': 'B5',
    'Simulation': 'B6',
    'Platformer': 'B7',
    'Adventure': 'B8',
    'Sport': 'B9'
}


def check_timestamp():
    """
    Check and compare timestamps between latest response and 
    latest completed response
    """
    timeStamps = RESPONSES.get_all_values()
    latestTime = timeStamps[-1][0]
    completedTimes = COMPLETED.get_all_values()
    latestCompleted = completedTimes[-1][0]
    print(latestTime)
    print(latestCompleted)
    if latestTime == latestCompleted:
        return False
    return True


def get_responses():
    """
    Collect the responses from the spreadsheet.
    Return the data for calculation for other spreadsheets
    """
    data = RESPONSES.get_all_values()
    for i in range(len(data)):
        data[i] = data[i][slice(1,4)]
    data = data[slice(1, (len(data)+1))]
    return data


def calculate_response_tally(data):
    """
    Gets each response made and calculates how many times
    the response was given
    """
    answers = TALLIES.get_all_values()
    for i in range(len(data[-1])):
        if data[-1][i] == ('Mobile' or 'PC' or 'Console'):
            continue
        else:
            answer = responseAnswers[data[-1][i]]
            tally = int(answers[answer][i+1])
            tally = tally + 1
            if i == 0:
                TALLIES.update(favouritesCells[data[-1][i]], tally)
            elif i == 1:
                TALLIES.update(leastCells[data[-1][i]], tally)


def tally_platform_choices(data):
    """
    Tally up the platform choice data and update
    the spreadsheet with the tally values
    """
    platform = SHEET.worksheet('Platform choice')
    answers = platform.get_all_values()
    answer = platformChoices[data[-1][2]]
    print(answers[answer])
    tally = int(answers[answer][1])
    tally = tally + 1
    platform.update(platformCells[data[-1][2]], tally)


def update_completed_checks():
    """
    Adds a timestamp to completed worksheet
    """
    timestamps = RESPONSES.get_all_values()
    timestamp = timestamps[-1][0]
    print(timestamp)
    COMPLETED.update('A2', timestamp)


def update_total_tally():
    """
    Updates response total tally
    """
    answers = TALLIES.get_all_values()
    answers = answers[slice(1, 10)]
    totalTally = SHEET.worksheet('Response total tally')
    for i in range(len(answers)):
        total = int(answers[i][1]) - int(answers[i][2])
        totalTally.update(tallyCells[answers[i][0]], total)


if check_timestamp():
    results = get_responses()
    calculate_response_tally(results)
    tally_platform_choices(results)
    update_completed_checks()
    update_total_tally()
