from enum import Enum
from player import *
from card import *
from board import *
from event import *
import random
import string

GameStatus = Enum(
    "GameStatus",
    [
        "WAITING",
        "START",
        "OVER",
    ],
)


class Game:
    def __init__(self):
        self.players = []
        self.winner = None
        self.game_turn = 0
        self.game_status = 0
        self.game_board = None
        self.deck = set()
        self.event_log = []
        self.demo = 0  # state to be set by a user during the demo

    # generates a random session id
    #  TODO: CHECK FOR COLLISIONS
    def gen_session_id(self):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(16))

    def get_state(self):
        player_states = []
        for player in self.players:
            player_states.append((player.get_state()))

        deck_states = []
        for card in self.deck:
            deck_states.append(card.get_state())

        game_state = [player_states,
                      deck_states,
                      self.game_board.get_state()]

        return game_state

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

    # ends the game
    def end_game(self, session_id):
        if self.get_player(session_id):
            self.game_status = GameStatus.OVER

    # accuse a player
    def accuse(self, session_id, character, weapon, room):
        player = self.get_player(session_id)
        if player == None:
            # HANDLE THIS
            pass

        # create the event for the accusation
        self.create_event(
            EventType.ACCUSE, session_id, None, character, room, weapon, None
        )

        # check if the guess was correct
        if sum([c.contains_clue(character, room, weapon) for c in self.deck]) == 3:
            self.create_event(EventType.WIN, session_id, None, None, None, None, None)
            self.end_game(session_id)
            return True
        else:
            self.create_event(EventType.LOSE, session_id, None, None, None, None, None)
            player.is_out = True
            return False

    # create an event
    def create_event(
        self, event_type, player1_id=None, player2_id=None, character=None, location=None, weapon=None, card=None
    ):
        event = Event(event_type, "", "")
        player1 = self.get_player(player1_id)
        player2 = self.get_player(player2_id)

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
            event.private_response = "{player} has finished their turn".format(
                player1.name
            )

        # event for a player being ready
        elif event_type == EventType.READY:
            event.private_response = "{player} is ready".format(player1.name)

        self.event_log.append(event)

        return True
    
    def end_turn(self, session_id):
        if self.get_player(session_id):
            self.game_turn = (self.game_turn + 1) % len(self.players)
            self.create_event(EventType.TURN, session_id)
            return True

    # Location is tuple containing coordinates of the location to move to
    def move_player(self, session_id, location):
        player = self.get_player(session_id)
        if player:
            ret = self.game_board.move_player(self, player.character, location)

            if ret:
                if (
                    self.game_board.get_room_type(location[0], location[1])
                    == RoomType.NORMAL
                ):
                    self.get_player(session_id).can_suggest = True

            return ret
        return False

    def get_available_moves(self, player):
        return self.game_board.get_valid_moves(player)

    def make_suggestion(self, session_id_accuser, session_id_accused, character, weapon, room, card):
        accuser = session_id_accuser
        accused = session_id_accused

        if self.can_suggest(self.get_player(accuser), weapon, room):
            self.create_event(self, EventType.SUGGEST, accuser,
                              accused, room, weapon)

        for player in self.players:
            if character in player.cards:
                self.create_event(self, EventType.SHOW, accuser,
                                  accused, None, None, None, card)
                break
            if weapon in player.cards:
                self.create_event(self, EventType.SHOW, accuser,
                                  accused, None, None, None, card)
                break
            if room in player.cards:
                self.create_event(self, EventType.SHOW, accuser,
                                  accused, None, None, None, card)
                break

    def can_suggest(self, session_id):
        player = self.get_player(session_id)
        if player == None:
            # HANDLE THIS
            pass
        return player.get_can_suggest()

    # will take in user input, process it, and then update game state accordingly
    def process_input(self, input):
        pass
