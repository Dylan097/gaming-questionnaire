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

response_answers = {
    'Strategy': 1,
    'RPG': 2,
    'FPS (First Person Shooter)': 3,
    'Action': 4,
    'TPS (Third Person Shooter)': 5,
    'Simulation': 6,
    'Platformer': 7,
    'Adventure': 8,
    'Sports': 9
}
favourites_cells = {
    'Strategy': 'B2',
    'RPG': 'B3',
    'FPS (First Person Shooter)': 'B4',
    'Action': 'B5',
    'TPS (Third Person Shooter)': 'B6',
    'Simulation': 'B7',
    'Platformer': 'B8',
    'Adventure': 'B9',
    'Sports': 'B10'
}
least_cells = {
    'Strategy': 'C2',
    'RPG': 'C3',
    'FPS (First Person Shooter)': 'C4',
    'Action': 'C5',
    'TPS (Third Person Shooter)': 'C6',
    'Simulation': 'C7',
    'Platformer': 'C8',
    'Adventure': 'C9',
    'Sports': 'C10'
}
platform_choices = {
    'Mobile': 0,
    'PC': 1,
    'Console': 2
}
platform_cells = {
    'Mobile': 'B1',
    'PC': 'B2',
    'Console': 'B3'
}
tally_cells = {
    'Strategy': 'B1',
    'RPG': 'B2',
    'FPS': 'B3',
    'Action': 'B4',
    'TPS': 'B5',
    'Simulation': 'B6',
    'Platformer': 'B7',
    'Adventure': 'B8',
    'Sports': 'B9'
}


def check_timestamp():
    """
    Check and compare timestamps between latest response and
    latest completed response
    """
    print('Comparing time stamps...\n')
    time_stamps = RESPONSES.get_all_values()
    times = [time_stamps[i][0] for i in range(len(time_stamps))]
    completed_times = COMPLETED.get_all_values()
    complete = [completed_times[i][0] for i in range(len(completed_times))]
    for i in range(len(times)):
        if i == 0:
            continue
        if len(complete) == 1:
            return i - 1
        for j in range(len(complete)):
            if j == 0:
                continue
            if times[i] == complete[j]:
                break
            if j == len(complete) - 1:
                print(f'{times[i]} is incomplete')
                return i - 1


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


def calculate_response_tally(data, time):
    """
    Gets each response made and calculates how many times
    the response was given
    """
    print('Calculating responses tally...\n')
    answers = TALLIES.get_all_values()
    response = data[time]
    for i in range(len(response)-1):
        answer = response_answers[response[i]]
        tally = int(answers[answer][i+1])
        tally = tally + 1
        if i == 0:
            print(f'Increasing {response[i]} favourites value...\n')
            TALLIES.update(favourites_cells[response[i]], tally)
            print(f'{response[i]} increased!\n')
        elif i == 1:
            print(f'Increasing {response[i]} least favourite value...\n')
            TALLIES.update(least_cells[response[i]], tally)
            print(f'{response[i]} increased!\n')
    print('Response tally calculated!\n')


def tally_platform_choices(data, time):
    """
    Tally up the platform choice data and update
    the spreadsheet with the tally values
    """
    print('Calculating platform choices...\n')
    platform = SHEET.worksheet('Platform choice')
    answers = platform.get_all_values()
    answer = platform_choices[data[time][2]]
    tally = int(answers[answer][1])
    tally = tally + 1
    platform.update(platform_cells[data[time][2]], tally)
    print('Platform choices calculated!\n')


def update_completed_checks(time):
    """
    Adds a timestamp to completed worksheet
    """
    print('Updating completed checks...\n')
    time_stamps = RESPONSES.get_all_values()
    time_stamp = [time_stamps[time+1][0]]
    COMPLETED.append_row(time_stamp)
    print('Updated completed checks!\n')


def update_total_tally():
    """
    Updates response total tally
    """
    print('Updating total tallies...\n')
    answers = TALLIES.get_all_values()
    answers = answers[slice(1, 10)]
    total_tally = SHEET.worksheet('Response total tally')
    for i in range(len(answers)):
        print(f'updating {answers[i][0]}...\n')
        total = int(answers[i][1]) - int(answers[i][2])
        total_tally.update(tally_cells[answers[i][0]], total)
        print(f'{answers[i][0]} updated!\n')


def main():
    """
    Run all program functions
    """
    while True:
        response = check_timestamp()
        if response is not None:
            results = get_responses()
            calculate_response_tally(results, response)
            tally_platform_choices(results, response)
            update_completed_checks(response)
            update_total_tally()
            print('All updates completed!\n')
        if input('Press any key to continue or e to exit program\n') == 'e':
            break


main()
