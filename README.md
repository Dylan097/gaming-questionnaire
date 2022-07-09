# Gaming Questionnaire

Gaming Questionnaire is a short questionnaire that, when complete, inputs answers to a google spreadsheet. 

The python for this questionnaire will compute the answers and return integers to the spreadsheet, telling the creator how many times each answer was given.

## How to use

When the developer console is open, it'll automatically update the oldest answer that hasn't been computed. Once that is computed, the creator just has to press enter to compute the next answer down the list (if there is any), or 'e' and then enter to exit the program.

## Features

### Existing Features

- Timestamp comparison
    - Compares each response timestamp and each completed timestamp to check which response hasn't been computed.
    - Once the program reaches a timestamp that hasn't been computed, it computes that response to the spreadsheet.

- Response calculation
    - Calculates each response and adds 1 to the appropriate tally on the spreadsheet, e.g. strategy as favourites adds 1 to the position 'B2' on the spreadsheet, platformer as least favourite adds 1 to the position 'C8' on the spreadsheet.

- Platform choice calculation
    - Calculates the answer given from the platform question and adds 1 to the appropriate tally

- Total tally calculation
    - Every computation will update every total in the total tally spreadsheet
    - The program takes the favourite and least favourite numbers from the 'Response tally' spreadsheet, and subtracts them to find the total preference.
    - The program returns a negative number if most people dislike the game type, a positive number if most people like the game type and a 0 if people like and dislike the game type about the same

- Updates the console
    - The program console updates using the print function to tell the program user what's currently being updated or checked
    - Gives the user an idea of where the program is currently at

### Future Features

- Automatic updates whenever a new response is given