import time
import requests


character = ""
session_id = ""
SERVER_ADDRESS = "http://127.0.0.1:5742/api/"
cards = []
board = []
current_room = ""
last_event_displayed = {}


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
        #TODO do accusation
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
            char = "Reverend Green"
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
            weapon = "Dagger"
        elif input == "3":
            weapon = "Pipe"
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

    #TODO make accusation to server
    requests.post(SERVER_ADDRESS + "make_accusation", json={'loc': loc, 'char': char, 'weapon': weapon})


def movementPhase():
    #TODO get movement options
    move_options = []
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
    move_location = int(input) - 1
    #TODO Send location data to server and print response saying succesfully updated location
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
            char = "Reverend Green"
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
        weapon = "Dagger"
    elif input == "3":
        weapon = "Pipe"
    elif input == "4":
        weapon = "Rope"
    elif input == "5":
        weapon = "Candlestick"
    elif input == "6":
        weapon = "Wrench"
    else:
        print("That was not a valid weapon")
        suggestionPhase(loc, char)
    #TODO make suggestion to server
    requests.post(SERVER_ADDRESS + "make_suggestion", json={'loc': loc, 'char': char, 'weapon': weapon})
    return 1


def canSuggest():
    #TODO can suggest
    return False


def printRow():
    row_1 = ""
    row_2 = ""
    row_3 = ""
    row_4 = ""
    row_5 = ""


def printBoard():
    print("BOARD")
    #TODO print board


def doTurn():
    #TODO do turn
    print("It is your turn")
    print("In your hand you have these cards: ")
    cardString = ""
    for card in cards:
        cardString = cardString + card + ", "
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
    resp = requests.post(SERVER_ADDRESS + "join_game", json={'username': "test"}).json()['session_id']
    session_id = resp['session_id']
    while character == "":
        available_chars = resp['available_characters']
        temp_char = selectChar(available_chars)
        resp2 = requests.post(SERVER_ADDRESS + "set_character", json={'session_id': session_id, "character": temp_char})
        print(resp2)
        print(resp2.json()['status'])
        if resp2.json()['status'] == 'Success':
            character = temp_char
    print("Do you want to start the game or wait for more players?")
    printMenu(["start", "wait"])
    #input = getInput(False)
    #TODO start game


def doGame():
    #TODO get status
    #requests.get("http://127.0.0.1:5742/api/get_game_state", params={'session_id': session_id})

    #TODO if status is your turn do turn
    doTurn()

    #time.sleep(2)


def main():
    startGame()
    doGame()

main()