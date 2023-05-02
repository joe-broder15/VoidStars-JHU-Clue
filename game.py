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
        self.game_status = GameStatus.WAITING
        self.game_board = None
        self.deck = []
        self.event_log = []
        self.demo = 0  # state to be set by a user during the demo

    # generates a random session id
    def gen_session_id(self):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(16))

    def start_game(self):
        self.game_status = GameStatus.START

        # make deck
        for i in WEAPON_CARDS:
            self.deck.append(Card(i, "weapon"))

        for i in ROOM_CARDS:
            self.deck.append(Card(i, "room"))

        for i in CHARACTERS:
            self.deck.append(Card(i, "character"))

        # get answer cards
        tmp = []
        random.shuffle(self.deck)
        for c in self.deck:
            if c.type == "weapon":
                print(c.name)
                tmp.append(c)
                self.deck.remove(c)
                break

        for c in self.deck:
            if c.type == "room":
                print(c.name)
                tmp.append(c)
                self.deck.remove(c)
                break

        for c in self.deck:
            if c.type == "character":
                print(c.name)
                tmp.append(c)
                self.deck.remove(c)
                break

        # deal cards to players
        p = 0
        while self.deck:
            self.players[p].cards.add(self.deck.pop())
            p = (p + 1) % len(self.players)

        # reset deck to the held out cards
        self.deck = tmp
        # start board
        self.game_board = Board()
        self.game_board.start_board([p.character for p in self.players])

        # start event
        self.create_event(EventType.START)

        return

    def get_state(self, session_id):

        if self.game_status == GameStatus.WAITING:
            player_states = [p.get_state(session_id) for p in self.players]
            event_states = [e.get_state(session_id) for e in self.event_log]

            game_state = {
                "players": player_states,
                "events": event_states,
                "board": None,
                "status": str(self.game_status),
                "turn": 0,
                "turn_character": None,
                "winner": self.winner,
            }
            return game_state

        player_states = [p.get_state(session_id) for p in self.players]
        event_states = [e.get_state(session_id) for e in self.event_log]

        win_name = None
        if not self.winner is None:
            win_name = self.winner.name
        game_state = {
            "players": player_states,
            "events": event_states,
            "board": self.game_board.get_state(),
            "status": str(self.game_status),
            "turn": self.game_turn,
            "turn_character": self.players[self.game_turn].character,
            "winner": win_name,
        }
        print(event_states)

        return game_state

    def get_ascii_board(self):
        ascii_board = self.game_board.get_ascii_board
        return ascii_board

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
            self.winner = player
            return True
        else:
            self.create_event(EventType.LOSE, session_id, None, None, None, None, None)
            player.is_out = True
            count = 0
            player_in = None
            for in_player in self.players:
                if not in_player.is_out:
                    count += 1
                    player_in = in_player
                if count > 1:
                    return False
            if count == 1:
                self.create_event(EventType.WIN, player_in.player_session_id, None, None, None, None, None)
                self.end_game(player_in.player_session_id)
            return False

    # create an event
    def create_event(
        self,
        event_type,
        player1_id=None,
        player2_id=None,
        character=None,
        location=None,
        weapon=None,
        card=None,
    ):
        event = Event(event_type, "", "")
        player1 = self.get_player(player1_id)
        player2 = self.get_player(player2_id)

        # create event for a player winning
        if event_type == EventType.WIN:
            event.public_response = "{} has won the game as {}".format(
                player1.name, player1.character
            )

        # create event for a player losing
        elif event_type == EventType.LOSE:
            event.public_response = (
                "{}'s accusation was false and is now out!".format(player1.name)
            )

        # event for a player moving
        elif event_type == EventType.MOVE:
            event.public_response = "{} has moved to the {}".format(
                character, location
            )

        # event for an accusation
        elif event_type == EventType.ACCUSE:
            event.public_response = "{player} has accused {character} of murder with the {weapon} in the {room}".format(
                player=player1.name,
                character=character,
                weapon=weapon,
                room=location,
            )

        # event for a suggestion
        elif event_type == EventType.SUGGEST:
            event.public_response = "{player} has suggested {character} commited murder with the {weapon} in the {room}".format(
                player=player1.name, character=character, weapon=weapon, room=location
            )

        # event for game start
        elif event_type == EventType.START:
            event.public_response = "The game has started!"

        # event for player added
        elif event_type == EventType.PLAYER_ADDED:
            event.public_response = (
                "{} has joined the game as {}".format(
                    player1.name, character
                )
            )

        # event for showing a card
        elif event_type == EventType.SHOW:
            public_response = "{} has shown {} a card".format(
                player2.character, player1.character
            )
            private_response = (
                "{} has shown {} they hold the {} card".format(
                    player2.name, player1.name, card
                )
            )
            private_ids = [player1.player_session_id, player2.player_session_id]
            event = Event(event_type, public_response, private_response, private_ids)

        # event for a turn being made
        elif event_type == EventType.TURN:
            event.public_response = "{} has finished their turn".format(
                player1.name
            )

        # event for a player being ready
        elif event_type == EventType.READY:
            event.public_response = "{} is ready".format(player1.name)

        elif event_type == EventType.STAY:
            event.public_response = "{} has stayed in the {}".format(character, location)

        self.event_log.append(event)

        return True

    def end_turn(self, session_id):
        if self.get_player(session_id):
            self.game_turn = (self.game_turn + 1) % len(self.players)
            while self.players[self.game_turn].is_out:
                self.game_turn = (self.game_turn + 1) % len(self.players)
            self.create_event(EventType.TURN, session_id)
            return True

    # Location is tuple containing coordinates of the location to move to
    def move_player(self, session_id, location):
        player = self.get_player(session_id)
        if player:
            if location == "STAY":
                self.create_event(EventType.STAY, character=player.character, location=location)
                return True
            if " " in location:
                location = location.replace(" ", "_")
            ret = self.game_board.move_player(player.character, location)
            pos = self.game_board.get_room_name_position(location)
            if ret:
                if (
                    self.game_board.get_room_type(pos[0], pos[1])
                    == RoomType.NORMAL
                ):
                    self.get_player(session_id).can_suggest = True
                else:
                    self.get_player(session_id).can_suggest = False
                self.create_event(
                    EventType.MOVE, character=player.character, location=location
                )

            return ret
        return False

    def get_available_moves(self, session_id):
        player = self.get_player(session_id)
        moves = self.game_board.get_valid_moves(player.character)
        if player.can_suggest:
            moves.append("Stay")
        return moves

    def make_suggestion(
        self, session_id_accuser, character, weapon, room
    ):
        accuser_character = session_id_accuser

        if self.can_suggest(session_id_accuser):
            self.get_player(accuser_character).can_suggest = False
            # Create SUGGEST event
            self.create_event(EventType.SUGGEST, session_id_accuser, character=character, location=room, weapon=weapon)

            # Move accused character to accuser's room if
            # the character is on the board
            all_characters = [player.character for player in self.players]
            location = room
            location = location.replace(" ", "_").upper()
            print(location)
            if character in all_characters:
                self.create_event(EventType.MOVE, None, None, character, room, None, None)
                self.game_board.teleport_player(character, location)
                for char_player in self.players:
                    if char_player.character == character:
                        char_player.can_suggest = True



            # For each other player, go through their cards and see if there's
            # a match with those in the suggestion
            # TODO: go through characters in clockwise order
            for player in self.players:
                if player.player_session_id == accuser_character:
                    continue
                else:
                    shown_card = None
                    if character in [card.name for card in player.cards]:
                        shown_card = character
                    elif weapon.lower() in [card.name for card in player.cards]:
                        shown_card = weapon
                    elif room.lower() in [card.name for card in player.cards]:
                        shown_card = room

                    if shown_card is not None:
                        self.create_event(
                            EventType.SHOW,
                            accuser_character,
                            player.player_session_id,
                            None,
                            None,
                            None,
                            shown_card,
                        )
                        return shown_card
            return None

    def can_suggest(self, session_id):
        player = self.get_player(session_id)
        if player is None:
            # HANDLE THIS
            return False
        return player.get_can_suggest()

    # will take in user input, process it, and then update game state accordingly
    def process_input(self, input):
        pass
