from enum import Enum

# TODO - CREATE SOME ENUMS SO WE AREN'T CONSTANTLY REFERING TO PLAYERS, ROOMS, AND CARDS AS NUMBERS

class Game:
    def __init__(self):
        """
        just listing out all the different pieces of information we will need to track,
        this in no way determined exctly which ones will merit their own members
        """
        self.players = None  # list of players
        self.board = None  # the board
        self.turn = None  # who's turn is it
        self.solutions = None  # solution cards
        self.playercards = None  # cards each player has in their hand
        self.weapons = None  # list of weapons
        self.out = None  # players who have already given accusations
        self.last = "" # a string decribing what the last move made was

    def get_state(self):
        return "this will eventually be some state", "this will eventually be some data"
    
    def get_turn(self):
        pass

    def move_player(self, player, location):
        pass

    def make_suggestion(self, player, suggestion):
        pass

    def make_accusation(self, player, suggestion):
        pass

    def end_game(self):
        pass

    # will take in user input, process it, and then update game state accordingly
    def process_input(self, input):
        pass
