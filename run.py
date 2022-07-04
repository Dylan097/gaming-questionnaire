import gspread
from google.oauth2.service_account import Credentials

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
    print('Comparing time stamps...\n')
    timeStamps = RESPONSES.get_all_values()
    latestTime = timeStamps[-1][0]
    completedTimes = COMPLETED.get_all_values()
    latestCompleted = completedTimes[-1][0]
    if latestTime == latestCompleted:
        print('TimeStamps are the same, rechecking...\n')
        return False
    print('TimeStamps different! Moving to next step...\n')
    return True


def get_responses():
    """
    Collect the responses from the spreadsheet.
    Return the data for calculation for other spreadsheets
    """
    print('Getting responses...\n')
    data = RESPONSES.get_all_values()
    for i in range(len(data)):
        data[i] = data[i][slice(1,4)]
    data = data[slice(1, (len(data)+1))]
    print('Responses recieved!\n')
    return data


def calculate_response_tally(data):
    """
    Gets each response made and calculates how many times
    the response was given
    """
    print('Calculating responses tally...\n')
    answers = TALLIES.get_all_values()
    for i in range(len(data[-1])):
        if data[-1][i] == 'Mobile' or 'PC' or 'Console':
            continue
        else:
            answer = responseAnswers[data[-1][i]]
            tally = int(answers[answer][i+1])
            tally = tally + 1
            if i == 0:
                print(f'Increasing {data[-1][i]} favourites value...\n')
                TALLIES.update(favouritesCells[data[-1][i]], tally)
                print(f'{data[-1][i]} increased!\n')
            elif i == 1:
                print(f'Increasing {data[-1][i]} least favourite value...\n')
                TALLIES.update(leastCells[data[-1][i]], tally)
                print(f'{data[-1][i]} increased!\n')
    print('Response tally calculated!\n')


def tally_platform_choices(data):
    """
    Tally up the platform choice data and update
    the spreadsheet with the tally values
    """
    print('Calculating platform choices...\n')
    platform = SHEET.worksheet('Platform choice')
    answers = platform.get_all_values()
    answer = platformChoices[data[-1][2]]
    tally = int(answers[answer][1])
    tally = tally + 1
    platform.update(platformCells[data[-1][2]], tally)
    print('Platform choices calculated!\n')


def update_completed_checks():
    """
    Adds a timestamp to completed worksheet
    """
    print('Updating completed checks...\n')
    timestamps = RESPONSES.get_all_values()
    timestamp = timestamps[-1][0]
    COMPLETED.update('A2', timestamp)
    print('Updated completed checks!\n')


def update_total_tally():
    """
    Updates response total tally
    """
    print('Updating total tallies...\n')
    answers = TALLIES.get_all_values()
    answers = answers[slice(1, 10)]
    totalTally = SHEET.worksheet('Response total tally')
    for i in range(len(answers)):
        print(f'updating {answers[i][0]}...\n')
        total = int(answers[i][1]) - int(answers[i][2])
        totalTally.update(tallyCells[answers[i][0]], total)
        print(f'{answers[i][0]} updated!\n')


def main():
    """
    Run all program functions
    """
    while True:
        if check_timestamp():
            results = get_responses()
            calculate_response_tally(results)
            tally_platform_choices(results)
            update_completed_checks()
            update_total_tally()
            print('All updates completed!\n')


main()
