"""
File to run different models of the game

Currently just a template file - the game class hasn't been written yet
"""
from GameClasses import *

"""
General Settings
"""
games_to_run = 100
turns_to_report = range(100)

list_of_cities = ['new york','washington','london','chicago','denver',
    'san francisco','atlanta','paris','st petersburg','johannesburg',
    'sao paolo','jacksonville','lagos','mexico city','los angeles',
    'buenos aires','bogota','santiago','lima','dar es salaam','istanbul',
    'tripoli','antanarivo','moscow','baghdad']

report_by_turn_keys = ['total_cubes_removed', 'total_cubes_removed_above_pop', 'total_hollow_men_dropped',
                       'total_hollow_men_pop_loss','unique_cities_with_hollow_men','special_player_cards_drawn'
                       'searchable_player_cards_drawn', 'epidemics_drawn']

report_by_game_keys = ['time to 8 cubes above pop', '1st epidemic turn', '2nd epidemic turn',
                       '3rd epidemic turn', '4th epidemic turn', '5th epidemic turn', '6th epidemic turn',
                       '7th epidemic turn', '8th epidemic turn', '9th epidemic turn', '10th epidemic turn',
                       ]

city_out_file = 'CityResults.csv'
turn_out_file = 'TurnResults.csv'
game_out_file = 'GameResults.csv'

#Open output files:
city_file = open(city_out_file)
turn_file = open(turn_out_file)
game_file = open(game_out_file)

#Print headers for the CSV files
city_header = 'Model Name,Run Number,Turn Number,Data,'
for city in list_of_cities:
    city_header += city + ','
city_header = city_header.lstrip(',')
city_header = city_header.strip(',')
city_file.write(city_header)

turn_header = 'Model Name,Run Number,Turn Number,'
for key in report_by_turn_keys:
    turn_header += key + ','
turn_header = turn_header.lstrip(',')
turn_header = turn_header.strip(',')
turn_file.write(turn_header)

game_header = 'Model Name, Run Number,'
for key in report_by_game_keys:
    game_header += key + ','
game_header = game_header.strip(',')
game_header = game_header.lstrip(',')
game_file.write(game_header)


"""
Execute Games
Baseline game should be our exact game settings at this point and represent Late June game
"""
model_name_1 = 'Baseline'
infection_deck_1 = 'InfectionDeck.txt''
player_deck_1 = 'PlayerDeck.txt''
execute_game(model_name_1, infection_deck_1, player_deck_1)

model_name_2 = 'Baseline - no hollow men'
infection_deck_2 = 'InfectionDeckNoHollowMen.txt'
player_deck_2 = 'PlayerDeck.txt'
execute_game(model_name_2, infection_deck_2, player_deck_2)

#Close Output Files
city_file.close()
turn_file.close()
game_file.close()

# Game Procs
def execute_game(model_name, infection_deck_path, player_deck_path):
    '''
    Run a model of games

    :param model_name: Name of the model to run
    :param infection_deck: The path to the file that is the description for the infection deck
    :param player_deck: The path to the file that is the description for the player deck
    :return:
    '''
    for game_num in range(games_to_run):
        inf_file = open(infection_deck_path)
        infection_deck = inf_file.read().splitlines()
        inf_file.close()

        player_deck = {}
        player_file = open('Player Deck.txt')
        for line in player_file.read().splitlines():
            # second element is the number of cards
            player_deck[line.split(',')[0]] = line.split(',')[1]

        p = PandemicGame(model_name, game_num, infection_deck, player_deck)

        game_end_found = 0
        turn_number = 1

        while game_end_found == 0:
            try:
                p.end_turn()
            except GameOverError:
                game_end_found = 0

            if turn_number in turns_to_report:
                record_turn_results(model_name, game_num, turn_number, p.status_report())

            turn_number += 1

        record_game_results(model_name, game_num, p.status_report())


def record_turn_results(model_name, game_num, turn_number, status_dict):
    '''
    Print the results to a CSV file that are interesting by turn.

    Things to capture:
        Number of cubes removed by city
        Number of hollow men dropped by city
        Hollow men population loss by city
        Unique cities with hollow men
        Total cubes removed
        Total Hollow men lost
        Total cubes removed over population
        Number of epidemics happened
        Upgraded player deck cards drawn
        Searchable cards drawn

    :param model_name: The name of the game to record
    :param game_num: The specific game number
    :param turn_number: The turn number for the game
    :param status_dict: a dump of the current status from the game object
    :return:
    '''

    report_by_city_keys = ['cubes_removed_by_city', 'hollow_men_dropped_by_city', 'hollow_men_pop_loss_by_city']

    for key in report_by_city_keys:

        printstr = ''
        printstr += model_name + ','
        printstr += game_num + ','
        printstr += turn_number + ','
        printstr += key + ','

        report_sum = 0

        report = status_dict.get(key,{})
        for city in list_of_cities:
            entry = report[key].get(city, 0)
            report_sum += entry
            printstr += entry + ','

        printstr += report_sum
        printstr = printstr.strip(',')
        printstr = printstr.lstrip(',')

        city_file.write(printstr)

    print_turnstr = ''
    print_turnstr += model_name + ','
    print_turnstr += game_num + ','
    print_turnstr += turn_number + ','

    for key in report_by_turn_keys:
        entry = status_dict.get(key,0)
        print_turnstr += str(entry) + ','

    printstr = print_turnstr.strip(',')
    printstr = print_turnstr.lstrip(',')

    turn_file.write(print_turnstr)


def record_game_results(model_name, game_num, status_dict):
    '''
    Print the results to a CSV file that are interesting at the end of the game

    Things to capture:
        Time to 8 cubes above population
        Time to first epidemic
        Time to second epidemic
        Time to third epidemic
        Time to fourth epidemic
        Time to fifth epidemic
        Time to sixth epidemic
        Time to seventh epidemic
        Time to eighth epidemic
        Time to ninth epidemic
        Time to tenth epidemic

    :param model_name: The name of the game to record
    :param game_num: The specific game number
    :param status_dict: a dump of the current status from the game object
    :return:
    '''

    print_gamestr = ''
    print_gamestr += model_name + ','
    print_gamestr += game_num + ','
    print_gamestr += status_dict.get('turns_to_8_cubes_above_pop','N/A') + ','

    epidemic_dict = status_dict.get('epidemic_timing', {})
    for epidemic_num in range(10):
        print_gamestr += epidemic_dict.get(epidemic_num, 'N/A') + ','

    printstr = print_gamestr.strip(',')
    printstr = print_gamestr.lstrip(',')

    game_file.write(print_gamestr)
