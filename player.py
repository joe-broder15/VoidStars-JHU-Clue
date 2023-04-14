CHARACTERS = [
    "Miss Scarlet",
    "Colonel Mustard",
    "Mrs. White",
    "Mr. Green",
    "Mrs. Peacock",
    "Professor Plum",
    "Mr. Body",
]


class Player:
    def __init__(self, player_session_id, name, character):
        self.player_session_id = player_session_id
        self.name = name
        self.cards = set()
        self.character = character
        self.can_suggest = True
        self.is_out = True

    # validate a session id
    def is_player(self, session_id):
        return self.player_session_id == session_id

    # check a session id and set a username
    def set_username(self, session_id, username):
        if not self.is_player(session_id):
            return False

        self.name = username
        return True

    # check a session id and set a character
    def set_character(self, session_id, character):
        if not self.is_player(session_id):
            return False

        self.character = character
        return True

    # check if the player has any card containing one of the provided clues
    def get_clue(self, character, location, weapon):
        for c in self.cards:
            if c.contains_clue(character, location, weapon):
                return c

    def get_state(self):
        cards = [c.get_state() for c in cards]
        return {
            "session_id": self.player_session_id,
            "name": self.name,
            "character": self.character,
            "can_suggest": self.can_suggest,
            "cards": cards,
        }
