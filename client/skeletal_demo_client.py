import time
import requests

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
        #Do accusation
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

    #Make accusation to server and respond to acurasy
    print(requests.post("http://127.0.0.1:5742/api/make_accusation", json={'loc': loc, 'char': char, 'weapon': weapon}).text)

def movementPhase():
    print("You are in a hallway. Where do you want to move:")
    printMenu(["Library", "Billiard Room"])
    input = getInput(True)
    if input == "accuse":
        return "accuse"
    moveLocation = ""
    if input == "1":
        moveLocation = "Library"
    elif input == "2":
        moveLocation = "Billiard Room"
    else:
        print("That was not a valid input")
        return movementPhase()
    #Send location data to server and print response saying succesfully updated location
    return moveLocation


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
    #Send loc, char, and weapon to server and print response
    print(requests.post("http://127.0.0.1:5742/api/make_suggestion", json={'loc': loc, 'char': char, 'weapon': weapon}).text)
    return 1


def simulateTurn():
    print("Movement Phase:")
    moveResult = movementPhase()
    if moveResult == "accuse":
        return
    print("Suggestion Phase:")
    suggestResult = suggestionPhase(moveResult)
    if suggestResult == 0:
        return
    print("Do you want to make a final accusation?")
    printMenu(["Yes", "No"])
    input = getInput(False)
    if input == "1":
        makeAccusation()
        return
    print("That is the end of your turn")


def waitForUpdate():
    print("Waiting for update")
    while True:
        #Get update from server and print it out. Update could be a randomly generated number or something to show this works on multiple clients at the same time.
        print(requests.get("http://127.0.0.1:5742/api/get_game_state", params={'game_id': 1}).text)
        time.sleep(2)

def homeMenu():
    while True:
        print("Do you want to:")
        printMenu(["Simulate a turn", "Wait for updates", "Leave"])
        action = getInput(False)
        if action == "1":
            simulateTurn()
        elif action == "2":
            waitForUpdate()
        elif action == "3":
            return


def main():
    print("Welcome to the Skeletal Demo:")
    homeMenu()

main()