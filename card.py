class Card:
    # constructor
    def __init__(self, name, cardType):
        self.name = name
        self.type = cardType

    # returns the card as json
    def get_state(self):
        return {"name": self.name, "type": self.type}

    # check whether the card is any of the provided arguments
    def contains_clue(self, character, location, weapon):
        return self.name in [character, location, weapon]