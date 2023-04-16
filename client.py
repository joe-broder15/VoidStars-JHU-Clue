import time
import requests
import copy

character = ""
session_id = ""
SERVER_ADDRESS = "http://127.0.0.1:5742/api/"
cards = []
board = []
current_room = ""
last_event_displayed = ""


def printMenu(menuList):
    i = 1
    for item in menuList:
        print(str(i) + ": " + item)
        i += 1


def getInput(allowAccus=False):
    if allowAccus:
        print("You can input accuse to go to an accusation.")
    inp = input("Please enter the number for the action you want to do\n")
    if allowAccus and inp.lower() == "accuse":
        makeAccusation()
        return "accuse"
    return inp


def makeAccusation(char="unentered", weapon="unentered"):
    loc = ""
    if char == "unentered":
        print("Who do you think did it?")
        printMenu(["Mrs. Peacock", "Colonel Mustard", "Reverend Green", "Professor Plum", "Miss Scarlet", "Mrs. White"])
        input = getInput()
        if input == "accuse":
            return 0
        if input == "1":
            char = "Mrs. Peacock"
        elif input == "2":
            char = "Colonel Mustard"
        elif input == "3":
            char = "Mr. Green"
        elif input == "4":
            char = "Professor Plum"
        elif input == "5":
            char = "Miss Scarlet"
        elif input == "6":
            char = "Mrs. White"
        else:
            print("That was not a valid character")
            makeAccusation()
    if weapon == "unentered":
        print("What weapon do you think they used?")
        printMenu(["Revolver", "Dagger", "Pipe", "Rope", "Candlestick", "Wrench"])
        input = getInput()
        if input == "accuse":
            return 0
        if input == "1":
            weapon = "Revolver"
        elif input == "2":
            weapon = "Knife"
        elif input == "3":
            weapon = "Lead Pipe"
        elif input == "4":
            weapon = "Rope"
        elif input == "5":
            weapon = "Candlestick"
        elif input == "6":
            weapon = "Wrench"
        else:
            print("That was not a valid weapon")
            makeAccusation(char)
    print("Where do you think it happened")
    printMenu(["Study", "Hall", "Lounge", "Library", "Billiard Room",
               "Dining Room", "Conservatory", "Ballroom", "Kitchen"])
    input = getInput()
    if input == "accuse":
        return 0
    if input == "1":
        loc = "Study"
    elif input == "2":
        loc = "Hall"
    elif input == "3":
        loc = "Lounge"
    elif input == "4":
        loc = "Library"
    elif input == "5":
        loc = "Billiard Room"
    elif input == "6":
        loc = "Dining Room"
    elif input == "7":
        loc = "Conservatory"
    elif input == "8":
        loc = "Ballroom"
    elif input == "9":
        loc = "Kitchen"
    else:
        print("That was not a valid location")
        makeAccusation(char, weapon)

    requests.post(SERVER_ADDRESS + "make_accusation", json={'session_id':session_id, 'room': loc, 'character': char, 'weapon': weapon})


def movementPhase():
    #TODO get movement options
    resp = requests.get(SERVER_ADDRESS + "get_available_moves", json={'session_id': session_id})
    move_options = resp.json()['availableMoves']
    if len(move_options) == 0:
        print("There are no available places to move to")
        return None
    print("You are in a " + current_room + ". Where do you want to move:")
    printMenu(move_options)

    input = getInput(True)
    if input == "accuse":
        return "accuse"
    if (not input.isdigit()) or int(input) < 1 or int(input) > len(move_options):
        print("That was not a valid input")
        return movementPhase()
    move_location = move_options[int(input) - 1]
    move_enum = move_options[int(input) - 1]
    move_enum.replace(" ", "_")
    resp = requests.post(SERVER_ADDRESS + "move_player", json={'session_id': session_id, 'location': move_enum.upper()})
    return move_location


def suggestionPhase(loc, char="unentered"):
    weapon = ""
    if char == "unentered":
        print("Who do you think did it?")
        printMenu(["Mrs. Peacock", "Colonel Mustard", "Reverend Green", "Professor Plum", "Miss Scarlet", "Mrs. White"])
        input = getInput(True)
        if input == "accuse":
            return 0
        if input == "1":
            char = "Mrs. Peacock"
        elif input == "2":
            char = "Colonel Mustard"
        elif input == "3":
            char = "Mr. Green"
        elif input == "4":
            char = "Professor Plum"
        elif input == "5":
            char = "Miss Scarlet"
        elif input == "6":
            char = "Mrs. White"
        else:
            print("That was not a valid character")
            suggestionPhase(loc)
    print("What weapon do you think they used?")
    printMenu(["Revolver", "Dagger", "Pipe", "Rope", "Candlestick", "Wrench"])
    input = getInput(True)
    if input == "accuse":
        return 0
    if input == "1":
        weapon = "Revolver"
    elif input == "2":
        weapon = "Knife"
    elif input == "3":
        weapon = "Lead Pipe"
    elif input == "4":
        weapon = "Rope"
    elif input == "5":
        weapon = "Candlestick"
    elif input == "6":
        weapon = "Wrench"
    else:
        print("That was not a valid weapon")
        suggestionPhase(loc, char)
    resp = requests.post(SERVER_ADDRESS + "make_suggestion", json={'session_id': session_id, 'location': loc, 'character': char, 'weapon': weapon})
    card = resp.json()['card']
    if not card == "None":
        print("You were shown the {} card".format(card))
    else:
        print("You were not shown any cards")
    return 1


def canSuggest():
    resp = requests.get(SERVER_ADDRESS + "can_suggest", json={'session_id': session_id}).json()
    return resp['canSuggest']


def printRow():
    row_1 = ""
    row_2 = ""
    row_3 = ""
    row_4 = ""
    row_5 = ""


def printBoard():
    print("BOARD")
    #TODO print board


def printEvents(events):
    event_copy = copy.deepcopy(events)
    if last_event_displayed != "":
        for event in events:
            if event != last_event_displayed:
                event_copy.pop(0)
            else:
                break
    else:
        print("EVENTS: ")
    for event2 in event_copy:
        print(event2["response"])

def doTurn():
    #TODO do turn
    print("It is your turn")
    print("In your hand you have these cards: ")
    cardString = ""
    for card in cards:
        cardString = cardString + card['name'] + ", "
    print(cardString[:-2])
    print("Here is the current board: ")
    printBoard()
    print("Movement Phase:")
    moveResult = movementPhase()
    if moveResult == "accuse":
        return
    if canSuggest():
        print("Suggestion Phase:")
        suggestResult = suggestionPhase(moveResult)
        if suggestResult == 0:
            return
    else:
        print("You are not allowed to suggest this turn")
    print("Do you want to make a final accusation?")
    printMenu(["Yes", "No"])
    input = getInput(False)
    if input == "1":
        makeAccusation()
        return
    print("That is the end of your turn")
    requests.post(SERVER_ADDRESS + "end_turn", json={'session_id': session_id})
    #TODO end turn


def selectChar(available_chars):
    print("Here are the available characters. Which one do you want?")
    printMenu(available_chars)
    input = getInput(False)
    if (not input.isdigit()) or int(input) < 1 or int(input) > len(available_chars):
        print("That was not a valid input")
        return selectChar(available_chars)
    return available_chars[int(input) - 1]

def startGame():
    global session_id
    global character
    print("Enter a username:")
    inputUsername = getInput(False)
    resp = requests.post(SERVER_ADDRESS + "join_game", json={'username': inputUsername}).json()['session_id']
    session_id = resp['session_id']
    while character == "":
        available_chars = resp['available_characters']
        temp_char = selectChar(available_chars)
        resp2 = requests.post(SERVER_ADDRESS + "set_character", json={'session_id': session_id, "character": temp_char})
        if resp2.json()['status'] == 'Success':
            character = temp_char
    print("Do you want to start the game or wait for more players?")
    printMenu(["start", "wait"])
    input = getInput(False)
    if input == "1":
        start_response = requests.post(SERVER_ADDRESS + "start_game", json={'session_id': session_id})
        print(start_response)


def doGame():
    global cards
    global board
    global current_room
    global last_event_displayed
    while True:
        state = requests.get(SERVER_ADDRESS + "get_game_state", json={'session_id': session_id}).json()['state']
        if state['status'] == "GameStatus.WAITING":
            printEvents(state['events'])
            last_event_displayed = state['events'][-1:]
            time.sleep(2)
            continue
        board = state['board']
        for room in board:
            if character in room['characters']:
                current_room = room['name']
        for player in state['players']:
            if player['character'] == character:
                cards = player['cards']
        printEvents(state['events'])
        last_event_displayed = state['events'][-1:][0]

        if state['status'] == "GameStatus.OVER":
            print("The game is over")
            return
        time.sleep(1)
        if state['turn_character'] == character:
            last_event_displayed = ""
            doTurn()
            last_event_displayed = ""
        time.sleep(1)


def main():
    startGame()
    doGame()

main()