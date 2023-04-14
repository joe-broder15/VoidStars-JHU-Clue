from enum import Enum
from player import *
from card import *
from event import *
import random
import string

class GameEngine:
    def __init__(self):
        self.players = []
        self.winner = None
        self.game_turn = 0
        self.game_status = 0
        self.game_board = None
        self.deck = set()
        self.event_log = []
        self.demo = 0  # state to be set by a user during the demo

    def gen_session_id(self, length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(16))

    def get_state(self):
        return "this will eventually be some state", self.demo

    # create a new player and generate a session id
    def add_player(self, username):
        # generate a session id
        session_id = self.gen_session_id()

        # make a new player and add them to the list of players
        p = Player(session_id, username, None)
        self.players.append(p)

        # list comprehension to build list of available characters
        available_characters = [c for c in CHARACTERS if self.is_char_avail(c)]

        return {
            "session_id": session_id,
            "available_characters": available_characters,
        }

    # get a player object by session id
    def get_player(self, session_id):
        for player in self.players:
            if player.is_player(session_id):
                return player
        return None

    # check if a character is available
    def is_char_avail(self, character):
        # iterate over all players and check if they are using the character
        for player in self.players:
            if player.character == character:
                return False
        return True

    # set a character
    def set_character(self, session_id, character):
        # try to get a player by session id
        player = self.get_player(session_id)

        # check if the player exists or if the character is available
        if player == None or not self.is_char_avail(character):
            return False

        # set character
        player.set_character(session_id, character)
        return True

    def end_game(self, session_id):
        pass

    def accuse(self, session_id, character, weapon, room):
        pass

    def create_event(
        self, event_type, player1, player2, character, location, weapon, card
    ):
        event = Event(event_type, "", "", [])

        # create event for a player winning
        if event_type == EventType.WIN:
            event.public_response = "{player} has won the game as {character}".format(
                player1.name, player1.character
            )

        # create event for a player losing
        elif event_type == EventType.LOSE:
            event.public_response = (
                "{player}'s accusation was false and is now out!".format(player1.name)
            )

        # event for a player moving
        elif event_type == EventType.MOVE:
            event.public_response = "{character} has moved to the {room}".format(
                character, location
            )

        # event for an accusation
        elif event_type == EventType.ACCUSE:
            event.public_response = "{player} has accused {character} of murder with the {weapon} in the {room}".format(
                player1.character,
                character,
                weapon,
                location,
            )

        # event for a suggestion
        elif event_type == EventType.SUGGEST:
            event.public_response = "{player} has suggested {character} commited murder with the {weapon} in the {room}".format(
                player1.character, character, weapon, location
            )

        # event for game start
        elif event_type == EventType.START:
            event.public_response = "The game has started!"

        # event for player added
        elif event_type == EventType.PLAYER_ADDED:
            event.public_response = (
                "{player} has joined the game as {character}".format(
                    player1.name, character
                )
            )

        # event for showing a card
        elif event_type == EventType.SHOW:
            event.public_response = "{player2} has shown {player1} a card".format(
                player2.character, player1.character
            )
            event.private_response = (
                "{player2} has shown {player1} they they hold the {card} card".format(
                    player2.character, player1.character, card
                )
            )
            event.private_IDs.append(player1.session_id)
            event.private_IDs.append(player2.session_id)

        # event for a turn being made
        elif event_type == EventType.TURN:
            event.private_IDs

        # event for a player being ready
        elif event_type == EventType.READY:
            event.private_response = "{player} is ready".format(player1.name)

        self.event_log.append(event)

        return True

    def move_player(self, player, location):
        pass

    def make_suggestion(self, player, suggestion):
        response = (
            "The player suggested {} used the {} in the {} to commit the crime".format(
                suggestion["char"], suggestion["weapon"], suggestion["loc"]
            )
        )
        print("FROM GAME SUBSYSTEM: " + response)
        return response

    # will take in user input, process it, and then update game state accordingly
    def process_input(self, input):
        pass
